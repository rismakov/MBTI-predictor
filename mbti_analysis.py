from __future__ import division, print_function
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import zipfile

import matplotlib.pyplot as plt
import seaborn as sns
# import plotly.offline as py
# import plotly.graph_objs as go
# py.init_notebook_mode(connected=True)


from stylometry_analysis import StyleFeatures

from Classifiers import Classifiers
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import average_precision_score, precision_score, recall_score, f1_score, accuracy_score
from sklearn.linear_model import LinearRegression

from xgboost import XGBClassifier
from BaselineClassifier import BaselineClassifier, MajorityBaselineClassifier

import ast

path = '../MBTI_project/featurized_mbti'

def featurize_data():
    zf = zipfile.ZipFile('../MBTI_project/mbti_1.csv.zip') 
    data = pd.read_csv(zf.open('mbti_1.csv'), encoding='utf-8')

    percents_of_each_type = data.groupby('type').count()['posts'] / sum(data.groupby('type').count()['posts']) * 100
    print('Sanity Check Passes: ', sum(percents_of_each_type) == 100)

    count = 1
    stylometry = []
    for mbti_type, posts in data['posts'].iteritems():
        print('Featurizing data point ', count) 
        stylometry.append(StyleFeatures(posts))
        print('Finished running data point ', count)
        count += 1

    # data['stylometry'] = [StyleFeatures(posts) for mbti_type, posts in data['posts'].iteritems()]
    data['stylometry'] = stylometry

    features = data['stylometry'][0]
    for feature in features:
        print(feature)
        data[feature] = [d[feature] for d in data['stylometry']]

    data.drop('stylometry', axis=1, inplace=True)
    print(data.columns)
    data.to_csv(path, encoding='utf-8')

if __name__ == "__main__":
    featurized_data = pd.read_csv(path, encoding='utf-8').drop(['Unnamed: 0', 'posts'], axis=1)
    print(featurized_data.columns)

    X = featurized_data.drop('type', axis=1)
    y = featurized_data['type']

    clfs = [
        # MLPClassifier(#{
             #'estimator__solver': 'adam', 
             #'estimator__activation': 'identity', 
             #'estimator__hidden_layer_sizes': (3,)
            #}
        #   ), 
        XGBClassifier(learning_rate= 0.1, n_estimators=100),
        # GradientBoostingClassifier(learning_rate=0.05, n_estimators=70),
        AdaBoostClassifier(learning_rate=0.2, n_estimators= 200),
        RandomForestClassifier(criterion= 'entropy', n_estimators=150),
        # DecisionTreeClassifier(),
        # LinearSVC(),
        # SVC(kernel='rbf'),
        LogisticRegression()
    ]

    multi_clfs = [
    #   BaselineClassifier(), MajorityBaselineClassifier()
    ]
    for clf in clfs:
        multi_clfs.append(OneVsRestClassifier(clf))

    mbti_model = Classifiers(multi_clfs, X, y)
    # mbti_model.print_cross_val_results()

    # RUN BELOW TO FEATURIZE DATA:
    # featurize_data()
    
    # RUN BELOW TO TRAIN MODEL:
    # flake8 --max-line-length 120

    # XGB, ABC, RF, LR
    params = [
        # Neural Network:
        # Best parameters: {'estimator__solver': 'adam', 'estimator__activation': 'identity', 'estimator__hidden_layer_sizes': (3,)}
        # Best score: 0.246439712464
        # {'estimator__hidden_layer_sizes': [(3, ), (7, )],  # [(3, ), (100, )], 
        # 'estimator__activation': ['identity'],  # ['relu', 'identity', 'logistic', 'tanh'],
        # 'estimator__solver': ['adam']  # ['adam', 'lbfgs', 'sgd'] 
        # },
        # XGBoost:
        # Best parameters: {'estimator__learning_rate': 0.1, 'estimator__n_estimators': 100}
        # Best score: 0.263800352638
        {'estimator__learning_rate': [0.05, 0.1, 0.2],  # [0.1, 0.2, 0.5, 1.0], 
         'estimator__n_estimators': [170, 200, 250]  # [100, 150, 200]
         },
        # Gradient Boosting:
        # Best parameters: {'estimator__learning_rate': 0.1, 'estimator__n_estimators': 50}
        # Best score: 0.246439712464
        # {'estimator__learning_rate': [0.05, 0.1],  # [0.1, 0.2, 0.5, 1.0], 
        # 'estimator__n_estimators': [50, 70],  # [10, 50, 100, 200]
        # },
        # Ada Boost:
        # Best parameters: {'estimator__learning_rate': 0.1, 'estimator__n_estimators': 100}
        # Best score: 0.25701885257
        {'estimator__learning_rate': [0.05, 0.1, 0.2],  # [0.1, 0.2, 0.5, 1.0], 
         'estimator__n_estimators': [100, 150, 200]  # [10, 50, 100, 200]
         },
        # Random Forest:
        # Best parameters: {'estimator__min_samples_split': 2, 'estimator__max_depth': None, 'estimator__criterion': 'gini', 'estimator__n_estimators': 100}
        # Best score: 0.258510782585
        {'estimator__n_estimators': [100, 150, 200],  # [10, 50, 100], 
         'estimator__criterion': ['gini', 'entropy']  # ['gini', 'entropy'], 
         # 'estimator__max_depth': [None, 5, 10], 
         # 'estimator__min_samples_split': [2, 0.3]
         },
        # LR:
        {
        'estimator__penalty': ['l1', 'l2'],
        'estimator__class_weight': [None, 'weighted']
        }

    ]

    mbti_model.train(save_model=True)
    # mbti_model.grid_search(params)
    
    # mbti_model.train()
    # mbti_model.test()
    # mbti_model.plot_roc_curve()
