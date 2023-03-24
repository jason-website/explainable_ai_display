import json

import pandas as pd
from adminui import *
from keras.models import load_model

from src.explainers import getExplainers, getOriginalData
from src.getData import getData, random_num

autoencoder = load_model('/Users/yingchao.ji/Desktop/tw/thesisProjects/explainable_ai_display/src/models/97.hdf5')
fraud, non_fraud, X_Train, Y_Train, x_test, df_original, X_test = getData()
lime_explainer, shap_explainer, train_columns = getExplainers(X_Train, Y_Train, autoencoder)

shap_plots = {}
app = AdminApp()

table_columns = [{'title': 'Index', 'dataIndex': 'number'}, {'title': 'Amount', 'dataIndex': 'Amount'},
                 {'title': 'Use Chip', 'dataIndex': 'Use Chip'}, {'title': 'Errors', 'dataIndex': 'Errors'},
                 {'title': 'Trans_hour', 'dataIndex': 'Trans_hour'},
                 {'title': 'Day_of_week', 'dataIndex': 'Day_of_week'},
                 {'title': 'MCC_Category', 'dataIndex': 'MCC_Category'},
                 {'title': 'Current Age', 'dataIndex': 'Current Age'},
                 {'title': 'Gender', 'dataIndex': 'Gender'}, {'title': 'hist_trans_60d', 'dataIndex': 'hist_trans_60d'},
                 {'title': 'hist_trans_24h', 'dataIndex': 'hist_trans_24h'},
                 {'title': 'hist_trans_avg_amt_60d', 'dataIndex': 'hist_trans_avg_amt_60d'},
                 {'title': 'Fraud', 'dataIndex': 'Fraud', 'filters': [{'text': 'Yes', 'value': 'Yes'},
                                                                      {'text': 'No', 'value': 'No'}]}]


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
    return NavigateTo("http://127.0.0.1:5000/charts/" + str(item['number']) + "/" + json.dumps(item))


def on_page(query):
    print(query)
    return TableResult(get_table_data(), 15, query['current_page'])


def on_modal_form_submit(form_data):
    print(form_data)
    return CloseModalForm()


@app.page('/', 'Table')
def table_page():
    return [
        Card(content=[
            DataTable("Example Table", columns=table_columns,
                      data=TableResult(get_table_data(), 15), on_data=on_page,
                      filter_form=FilterForm([
                          SelectBox('Fraud', data=['Yes', 'No'], placeholder="Yes")
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