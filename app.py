import pandas as pd
from flask import Flask, render_template
import base64

from src.explainers import generateHtml, getExplainers, getOriginalData
from src.getData import getData, random_num

from keras.models import Model, load_model

app = Flask(__name__)

autoencoder = load_model('/Users/yingchao.ji/Desktop/tw/thesisProjects/explainable_ai_display/src/models/97.hdf5')
fraud, non_fraud, X_Train, Y_Train, x_test,df_original, X_test = getData()
lime_explainer, shap_explainer, train_columns = getExplainers(X_Train, Y_Train, autoencoder)

shap_plots = {}

@app.route('/')
def home():
    merged_df = pd.DataFrame()
    numbers=random_num(fraud, non_fraud)
    for i in numbers:
        merged_df=pd.concat([getOriginalData(i,df_original,X_test),merged_df])
    df_html=merged_df.to_html()
    return render_template("home.html",df_html=df_html)



@app.route('/explanations')
def get_explanations():
    num = 100
    df=getOriginalData(num, df_original, X_test)
    # 将 DataFrame 转换为 HTML 表格
    table_html = df.to_html(classes='table')
    exp_html, shap_html = generateHtml(num, lime_explainer, shap_explainer, train_columns, x_test, autoencoder)
    shap_plots[0] = exp_html
    shap_plots[1] = shap_html
    return render_template('explanations.html', shap_plots=shap_plots, table_html=table_html)


if __name__ == '__main__':
    app.run(debug=True)
