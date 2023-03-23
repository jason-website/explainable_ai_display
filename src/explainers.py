import lime
import shap
import lime.lime_tabular


def getExplainers(X_Train, Y_Train, autoencoder):
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(X_Train.values.astype('float32'), training_labels=Y_Train,
                                                            feature_names=list(X_Train.columns),
                                                            class_names=['No Fraud', 'Fraud'], mode='classification')
    shap.initjs()
    shap_explainer = shap.KernelExplainer(lambda x: autoencoder.predict(x), X_Train.sample(n=50, random_state=1))
    return lime_explainer, shap_explainer, X_Train.columns


def generateHtml(num, lime_explainer, shap_explainer, train_columns, x_test, autoencoder):
    record = x_test[x_test['New_ID'] == num].drop(columns=['New_ID'])
    choosen_instance = record.values[0]
    exp_html = lime_explainer.explain_instance(choosen_instance, lambda x: autoencoder.predict(x).astype(float),
                                               num_features=7).as_html()
    shap_values = shap_explainer.shap_values(choosen_instance, nsamples=500)
    force_plot = shap.force_plot(shap_explainer.expected_value[0], shap_values[1], choosen_instance,
                                 feature_names=train_columns, show=True, matplotlib=False)
    shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"
    return exp_html, shap_html


def getOriginalData(num, df_original, X_test):
    columns1=['Amount','Use Chip','Errors','Trans_hour','Day_of_week','MCC_Category','Current Age','Gender','hist_trans_60d','hist_trans_24h','hist_trans_avg_amt_60d','Fraud']
    columns2=['Amount/交易额','Use Chip/是否线上交易','Errors/卡片是否有技术问题','Trans_hour/几点转账','Day_of_week/周几转账','MCC_Category/购物类别','Current Age/用户当前年龄','Gender/用户性别','hist_trans_60d/前60天此卡交易数','hist_trans_24h/前24小时此卡交易数','hist_trans_avg_amt_60d/前60天平均交易量','Fraud是否为欺诈']
    # columns2=['交易额\n\nhe','是否线上交易','卡片是否有技术问题','几点转账','周几转账','购物类别','用户当前年龄','用户性别','前60天此卡交易数','前24小时此卡交易数','前60天平均交易量']
    dic1=dict(zip(columns1,columns1))
    dic2=dict(zip(columns1,columns2))
    column_type=1
    df_show = df_original[df_original['index'] == X_test.iloc[int(num), 0]]
    df_show.set_index('index', inplace=True)
    return df_show.rename(columns=eval('dic' + str(column_type)))[eval('columns' + str(column_type))].head(1).fillna(
        'no error')
