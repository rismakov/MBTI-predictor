from __future__ import division, print_function

import pandas as pd
import time

from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

import tensorflow as tf
from tensorflow import keras

from baseline_clf import BaselineClassifier, MajorityBaselineClassifier
from classifier_runner import Classifiers
from utils.constants import LABEL_COL, NUM_OF_TYPES, RANDOM_STATE, TEXT_COL
from utils.utils import open_concat_data, remove_negative_values


num_partitions = 10  # number of partitions to split dataframe
num_cores = 4  # number of cores on your machine


def cross_validate_and_print_results(clfs, X, y):
    mbti_model = Classifiers(clfs, X, y)
    mbti_model.print_cross_val_results()


def grid_search(clfs, params):
    mbti_model = Classifiers(clfs, X, y)
    mbti_model.grid_search(params)


def run_models(clfs):
    pass


if __name__ == "__main__":
    # RUN BELOW TO FEATURIZE DATA:
    start_time = time.time()

    data = open_concat_data()
    X = data.drop([LABEL_COL], axis=1)
    y = data[LABEL_COL]

    tf_model = keras.Sequential([
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    X['polarity'] = X['polarity'] + 1  # remove negative values

    clfs = [
        # tf_model,
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

    cross_validate_and_print_results(multi_clfs, X, y)

    '''
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

    # grid_search(multi_clfs_to_gs, params)

    # mbti_model.train(save_model=True)
    # mbti_model.grid_search(params)

    # mbti_model.train()
    # mbti_model.test()
    # mbti_model.plot_roc_curve()

    seconds = time.time() - start_time
    minutes = seconds / 60
    print("Featurizer took", minutes, "minutes to run")
    '''
