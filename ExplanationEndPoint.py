import json
import os.path

from adminui import *
from keras.models import load_model
from src.explainers import getOriginalData, generateHtml, getExplainers
from src.getData import getData
from flask import Flask, render_template
import pandas as pd

SRC_MODELS__HDF_ = './src/models/97.hdf5'

app = Flask(__name__)
current_dir = os.path.dirname(__file__)
autoencoder = load_model(os.path.join(current_dir, SRC_MODELS__HDF_))
X_Train = pd.read_csv('temp/X_Train.csv', index_col=0)
Y_Train = pd.read_csv('temp/Y_Train.csv', index_col=0)
df_original = pd.read_csv('temp/df_original.csv', index_col=0)
X_test = pd.read_csv('temp/X_test.csv', index_col=0)
x_test = pd.read_csv('temp/x_test_new_id.csv', index_col=0)
lime_explainer, shap_explainer, train_columns = getExplainers(X_Train, Y_Train, autoencoder)

shap_plots = {}


@app.route('/charts/<number>')
def form_page(number):
    num = int(number)
    df = getOriginalData(number, df_original, X_test)
    # 将 DataFrame 转换为 HTML 表格
    table_html = df.to_html(classes='table')
    exp_html, shap_html = generateHtml(num, lime_explainer, shap_explainer, train_columns, x_test, autoencoder)
    shap_plots[0] = exp_html
    shap_plots[1] = shap_html
    return render_template('explanations.html', shap_plots=shap_plots, table_html=table_html)


if __name__ == '__main__':
    app.run()
