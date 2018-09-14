from __future__ import division, print_function

import numpy as np
import pandas as pd
import zipfile

from Classifiers import Classifiers
from multiprocessing import Pool

from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from baseline_clf import BaselineClassifier, MajorityBaselineClassifier
from stylometry_analysis import StyleFeatures

path = '../MBTI_project/featurized_mbti'

num_partitions = 10  # number of partitions to split dataframe
num_cores = 4  # number of cores on your machine


def add_stylometry_info(data):
    data['stylometry'] = data['posts'].apply(lambda x: StyleFeatures(x))
    return data


def parallelize_dataframe(df, func):
    print('Spliting data.')
    df_split = np.array_split(df, num_partitions)
    print('Pooling data.')
    pool = Pool(num_cores)
    print('Concatenating data.')
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    print('Joining data.')
    pool.join()
    return df


def featurize_data():
    zf = zipfile.ZipFile('../MBTI_project/mbti_1.csv.zip') 
    data = pd.read_csv(zf.open('mbti_1.csv'), encoding='utf-8')

    percents_of_each_type = data.groupby('type').count()['posts'] / sum(data.groupby('type').count()['posts']) * 100
    print('Sanity Check Passes: ', sum(percents_of_each_type) == 100)

    data = parallelize_dataframe(data, add_stylometry_info)

    features = data['stylometry'][0]
    for feature in features:
        print(feature)
        data[feature] = [d[feature] for d in data['stylometry']]

    data.drop('stylometry', axis=1, inplace=True)
    print(data.columns)
    data.to_csv(path, encoding='utf-8')


def open_data():
    featurized_data = pd.read_csv(path, encoding='utf-8').drop(['Unnamed: 0', 'posts'], axis=1)
    X = featurized_data.drop(['type', 'avg_post_len', 'mean_sentence_len', 'std_sentence_len'], axis=1)
    y = featurized_data['type']

    return X, y


def cross_validate_and_print_results(clfs):
    X, y = open_data()

    mbti_model = Classifiers(clfs, X, y)
    mbti_model.print_cross_val_results()


if __name__ == "__main__":
    # RUN BELOW TO FEATURIZE DATA:
    # featurize_data()
    
    clfs = [
        MLPClassifier(), 
        XGBClassifier(learning_rate=0.1, n_estimators=100),
        GradientBoostingClassifier(learning_rate=0.05, n_estimators=70),
        AdaBoostClassifier(learning_rate=0.2, n_estimators=200),
        RandomForestClassifier(criterion='entropy', n_estimators=150),
        DecisionTreeClassifier(),
        LinearSVC(),
        # SVC(kernel='rbf'),
        LogisticRegression(),
        MultinomialNB()
    ]

    multi_clfs = [BaselineClassifier(), MajorityBaselineClassifier()]
    for clf in clfs:
        multi_clfs.append(OneVsRestClassifier(clf))

    cross_validate_and_print_results(multi_clfs)

    '''
    # RUN BELOW TO TRAIN MODEL:
    # flake8 --max-line-length 120

    # XGB, ABC, RF, LR
    params = [
        # Neural Network:
        # Best parameters: {'estimator__solver': 'adam', 'estimator__activation': 
                            'identity', 'estimator__hidden_layer_sizes': (3,)}
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
        # Best parameters: {'estimator__min_samples_split': 2, 'estimator__max_depth': None, 
                            'estimator__criterion': 'gini', 'estimator__n_estimators': 100}
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

    # mbti_model.train(save_model=True)
    # mbti_model.grid_search(params)
    
    # mbti_model.train()
    # mbti_model.test()
    # mbti_model.plot_roc_curve()
    '''
