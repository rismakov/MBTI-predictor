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

PATH = '../MBTI_project/featurized_mbti'

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
    data.to_csv(PATH, encoding='utf-8')


def open_data():
    featurized_data = pd.read_csv(PATH, encoding='utf-8').drop(['Unnamed: 0', 'posts'], axis=1)
    X = featurized_data.drop(['type', 'avg_post_len', 'mean_sentence_len', 'std_sentence_len'], axis=1)
    y = featurized_data['type']

    # Because Naive Bayes doesnt accept negative values: 
    X['polarity'] = X['polarity'] + 1

    return X, y


def cross_validate_and_print_results(clfs):
    X, y = open_data()

    mbti_model = Classifiers(clfs, X, y)
    mbti_model.print_cross_val_results()
    


def grid_search(clfs, params):
    X, y = open_data()

    mbti_model = Classifiers(clfs, X, y)
    mbti_model.grid_search(params)

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

    # cross_validate_and_print_results(multi_clfs)

    clfs_to_grid_search = [XGBClassifier(), AdaBoostClassifier()]
    multi_clfs_to_gs = []
    for clf in clfs_to_grid_search:
        multi_clfs_to_gs.append(OneVsRestClassifier(clf))

    params = [
        {'estimator__learning_rate': [0.2, 0.25, 0.3, 0.5],  # [0.05, 0.1, 0.2, 0.25] - 0.25,
         'estimator__n_estimators': [50, 60, 70, 100]  # [70, 100, 150, 200, 300] - 70
        },
        {'estimator__learning_rate': [0.2, 0.25, 0.3, 0.5], # [0.05, 0.1, 0.2, 0.25] -0.25,
         'estimator__n_estimators': [200, 250, 300, 400] # [70, 100, 150, 200, 300] - 300
        },
    ]
    
    grid_search(multi_clfs_to_gs, params)

    # mbti_model.train(save_model=True)
    # mbti_model.grid_search(params)
    
    # mbti_model.train()
    # mbti_model.test()
    # mbti_model.plot_roc_curve()

