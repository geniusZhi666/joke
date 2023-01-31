# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 19:10:50 2023

@author: Zhi
"""

# import modules
import pandas as pd
from sklearn import tree
import graphviz
import numpy as np

from sklearn.preprocessing import LabelEncoder
# read data from other places, e.g. csv
# drop_list: variables that are not used
def read_data(file_path, drop_list=[]):
    dataSet = pd.read_csv(file_path,sep=',')
    for col in drop_list:
        dataSet = dataSet.drop(col,axis=1)
    return dataSet

# read data in csv format
file_path = "tree_data.csv"
dataSet = read_data(file_path,["User id"])
target_var = 'Buying'

df1 = dataSet.copy()

for i in range(len(dataSet)):
    if dataSet["Age"][i]=="<=30":
        dataSet["Age"][i]=0
    elif dataSet["Age"][i]=="[31,40]":
        dataSet["Age"][i]=1
    else:
        dataSet["Age"][i]=2
    if dataSet["Incoming"][i]=="low":
        dataSet["Incoming"][i]=0
    elif dataSet["Incoming"][i]=="medium":
        dataSet["Incoming"][i]=1
    else:
        dataSet["Incoming"][i]=2
    if dataSet["Student"][i]=="no":
        dataSet["Student"][i]=0
    else:
        dataSet["Student"][i]=1
    if dataSet["Credit Rating"][i]=="fair":
        dataSet["Credit Rating"][i]=0
    else:
        dataSet["Credit Rating"][i]=1
    if dataSet["Buying"][i]=="no":
        dataSet["Buying"][i]=0
    else:
        dataSet["Buying"][i]=1


clf = tree.DecisionTreeClassifier()
clf = clf.fit(dataSet.iloc[:, 0:-1], dataSet[target_var].astype('int'))



# 特征列名
data_feature_name = df1.columns[:-1]
# 标签分类
data_target_name = np.unique(df1["Buying"])

dot_data = tree.export_graphviz(clf, out_file=None,
                                feature_names=dataSet.columns[:-1], # 特征名称
                                class_names=['No', 'Yes'], # 目标变量的类别名
                               filled=True, rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)
graph.render('example.gv',view=True)
print('Save example.gv file!\n')

y_prob = clf.predict_proba([[2,1,0,1]])[:,1]
