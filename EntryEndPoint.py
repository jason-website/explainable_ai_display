import json
import os.path

import pandas as pd
import os
from adminui import *
from keras.models import load_model

from src.explainers import getExplainers, getOriginalData
from src.getData import getData, random_num

current_dir = os.path.dirname(__file__)
autoencoder = load_model(os.path.join(current_dir, './src/models/97.hdf5'))
fraud, non_fraud, X_Train, Y_Train, x_test, df_original, X_test = getData()
lime_explainer, shap_explainer, train_columns = getExplainers(X_Train, Y_Train, autoencoder)

shap_plots = {}
app = AdminApp(use_fastapi=True)
app.app_title = "Explainable AI methods for credit card fraud detection: Evaluation of LIME and SHAP through a User Study"
app.copyright_text = 'Yingchao Ji'
app.footer_links = {
    'Thesis from Diva DataBase': 'https://www.diva-portal.org/smash/record.jsf?pid=diva2%3A1626230&dswid=-3187'}
fastapi_app = app.prepare()
table_columns = [{'title': 'Index', 'dataIndex': 'number'}, {'title': 'Amount', 'dataIndex': 'Amount'},
                 {'title': 'Use Chip', 'dataIndex': 'Use Chip'}, {'title': 'Errors', 'dataIndex': 'Errors'},
                 {'title': 'Trans_hour', 'dataIndex': 'Trans_hour'},
                 {'title': 'Day_of_week', 'dataIndex': 'Day_of_week'},
                 {'title': 'MCC_Category', 'dataIndex': 'MCC_Category'},
                 {'title': 'Current Age', 'dataIndex': 'Current Age'},
                 {'title': 'Gender', 'dataIndex': 'Gender'}, {'title': 'hist_trans_60d', 'dataIndex': 'hist_trans_60d'},
                 {'title': 'hist_trans_24h', 'dataIndex': 'hist_trans_24h'},
                 {'title': 'hist_trans_avg_amt_60d', 'dataIndex': 'hist_trans_avg_amt_60d'},
                 {'title': 'Fraud', 'dataIndex': 'Fraud'}]


def get_table_data():
    merged_df = pd.DataFrame()
    numbers = random_num(fraud, non_fraud)
    for i in numbers:
        original_data = getOriginalData(i, df_original, X_test)
        original_data['number'] = i
        merged_df = pd.concat([original_data, merged_df])
    data = merged_df.to_json(orient='records')
    return json.loads(data)


def on_edit(item):
    host_address = os.environ.get('HOST_ADDRESS')
    print("Host address is:", host_address)
    return NavigateTo(f"http://{host_address}:5000/charts/" + str(item['number']) + "/" + json.dumps(item))


def on_page(query):
    new_data = get_table_data()
    print(query)
    try:
        fraud_value = query['formValues']['fraud']
        filter_data = [d for d in new_data if d.get('Fraud') == fraud_value]
        return TableResult(filter_data, 10, query['current_page'])
    except KeyError:
        return TableResult(new_data, 15, query['current_page'])


@app.page('/', 'Table')
def table_page():
    return [
        Card(content=[
            DataTable("Example Table", columns=table_columns,
                      data=TableResult(get_table_data(), 15), on_data=on_page,
                      filter_form=FilterForm([
                          SelectBox('Fraud', data=['Yes', 'No'], placeholder="Choose Yes Or No")
                      ], submit_text='Filter', reset_text='Clear'),
                      row_actions=[
                          TableRowAction('edit', 'Check Explanations', on_click=on_edit),
                      ])
        ])
    ]


app.set_as_shared_app()  # set the app as the shared app, so it can be accessed globally
import ExplanationEndPoint

if __name__ == '__main__':
    app.run(port=5001)
