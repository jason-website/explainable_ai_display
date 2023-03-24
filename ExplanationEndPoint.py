import json

from adminui import *
from keras.models import load_model
from src.explainers import getOriginalData, generateHtml, getExplainers
from src.getData import getData
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
autoencoder = load_model('/Users/yingchao.ji/Desktop/tw/thesisProjects/explainable_ai_display/src/models/97.hdf5')
fraud, non_fraud, X_Train, Y_Train, x_test, df_original, X_test = getData()
lime_explainer, shap_explainer, train_columns = getExplainers(X_Train, Y_Train, autoencoder)

shap_plots = {}

@app.route('/charts/<number>/<data>')
def form_page(number, data):
    num = int(number)
    data = json.loads(data)
    df = pd.json_normalize(data)
    # 将 DataFrame 转换为 HTML 表格
    table_html = df.to_html(classes='table')
    exp_html, shap_html = generateHtml(num, lime_explainer, shap_explainer, train_columns, x_test, autoencoder)
    shap_plots[0] = exp_html
    shap_plots[1] = shap_html
    return render_template('explanations.html', shap_plots=shap_plots, table_html=table_html)


if __name__ == '__main__':
    app.run()
