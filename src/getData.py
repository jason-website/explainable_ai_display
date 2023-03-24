import random

import pandas as pd
from pylab import rcParams
from keras.models import load_model
from sklearn.model_selection import train_test_split


def getData():
    rcParams['figure.figsize'] = 14, 8
    df_o = pd.read_csv(
        "/Users/yingchao.ji/Desktop/tw/thesisProjects/explainable_ai_display/src/dataset/data_preprosing_month_hist_encode_standarize.csv")
    df_o = df_o.drop(columns=['Latitude', 'Longitude', 'hist_fraud_trans_24h'])
    df2 = df_o
    cnt_non_fraud = df2[df2['Fraud'] == 0]['Amount'].count()
    df2_class_fraud = df2[df2['Fraud'] == 1]
    df2_class_nonfraud = df2[df2['Fraud'] == 0]
    # OverSampling
    df2_class_fraud_oversample = df2_class_fraud.sample(cnt_non_fraud, replace=True)
    df2_oversampled = pd.concat([df2_class_nonfraud, df2_class_fraud_oversample], axis=0)
    df = df2_oversampled

    X = df.drop(columns=['Fraud'])
    Y = df[['Fraud']]
    X_train, X_test, Y_train, Y_Test = train_test_split(X, Y, test_size=0.30, random_state=101)
    X_train = X_train.drop(columns=['index'])
    X_Train, Y_Train = X_train, Y_train

    df_original = pd.read_csv(
        "/Users/yingchao.ji/Desktop/tw/thesisProjects/explainable_ai_display/src/dataset/data_preprosing_month_hist.csv")
    columns = ['index', 'Amount', 'Use Chip', 'Errors', 'Fraud', 'Trans_hour', 'Day_of_week', 'MCC_Category',
               'Current Age', 'Gender', 'Latitude', 'Longitude', 'hist_trans_60d', 'hist_trans_24h',
               'hist_fraud_trans_24h', 'hist_trans_avg_amt_60d']
    df_original = df_original[columns].drop(columns=['Latitude', 'Longitude', 'hist_fraud_trans_24h'])
    x_test = X_test.drop(columns=['index'])

    test = Y_Test.rename(columns={'Fraud': 'Class'})
    test['New_ID'] = range(0, len(test))
    x_test['New_ID'] = range(0, len(X_test))
    fraud = test[test['Class'] == 1]
    non_fraud = test[test['Class'] == 0]
    return fraud, non_fraud, X_Train, Y_Train, x_test, df_original, X_test


def random_num(fraud, non_fraud):
    RANDOM_SEED = 42
    LABELS = ["Normal", "Fraud"]
    f_l = len(fraud)
    n_f_l = len(non_fraud)
    result = []
    for i in range(3):
        result.append(fraud.iloc[random.randint(0, f_l)].New_ID)
        result.append(fraud.iloc[random.randint(0, f_l)].New_ID)
        result.append(fraud.iloc[random.randint(0, f_l)].New_ID)
        result.append(non_fraud.iloc[random.randint(0, n_f_l)].New_ID)
        result.append(non_fraud.iloc[random.randint(0, n_f_l)].New_ID)
    return result
    # 假设您已经准备好了您的数据和模型，这里只展示如何生成LIME的结果
