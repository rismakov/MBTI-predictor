import numpy as np
from random import choice


class BaselineClassifier(object):
    '''Classifier that randomly predicts label. Takes into account the probability of getting each label.
    '''
    def __init__(self):
        self.name = 'Baseline'

    def fit(self, X, y):
        self._y = y

    def predict(self, X):
        return [choice(list(self._y)) for i in range(X.shape[0])]

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
        cnts = {}
        for label in self._y_sample.unique():
            cnt = list(self._y_sample).count(label)
            cnts[cnt] = label
        return cnts[max(cnts)]

    def fit(self, X, y):
        self._y_sample = y
        self._majority_class = self.get_majority_class()

    def predict(self, X):
        return [self._majority_class] * X.shape[0]

    def get_params(self, deep=False):
        return {}
