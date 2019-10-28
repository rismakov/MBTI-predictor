from __future__ import division

import logging
from random import choice

import numpy as np


class BaselineClassifier(object):
    '''Classifier that randomly predicts label based on probability of getting each label.
    '''
    
    def __init__(self):
        self.name = 'Baseline'

    def fit(self, X, y):
        logging.info(
            'Fitting {} labels for {} classifier'.format(len(y), self.name)
        )

        self._X = X
        self._values = list(set(y))
        logging.info('{} unique label values'.format(len(self._values)))

        self._p = [list(y).count(value) / len(y) for value in self._values]

    def predict(self, X):
        return np.random.choice(self._values, X.shape[0], p=self._p)

    def get_params(self, deep=False):
        return {}


class MajorityBaselineClassifier(object):
    '''Classifier that predicts majority class every time.
    '''
    
    def __init__(self):
        self.name = 'MajorityBaseline'

    def get_majority_class(self):
        '''Returns the label that appears most frequently in y.
        '''
        labels, counts = np.unique(self._y_sample, return_counts=True)
        max_count_ind = list(counts).index(max(counts))

        return labels[max_count_ind]

    def fit(self, X, y):
        logging.info(
            'Fitting {} labels for {} classifier'.format(len(y), self.name)
        )

        self._y_sample = y
        self._majority_class = self.get_majority_class()

    def predict(self, X):
        return [self._majority_class] * X.shape[0]

    def get_params(self, deep=False):
        return {}
