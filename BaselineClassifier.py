from random import choice

class BaselineClassifier(object):
    def __init__(self):
        self.name = 'Baseline'

    def fit(self, X, y):
        self._X = X
        self._y = y

    def predict(self, X):
        return [choice(list(self._y)) for i in xrange(X.shape[0])]

    def get_params(self, deep=False):
        return {}


class MajorityBaselineClassifier(object):
    def __init__(self):
        self.name = 'MajorityBaseline'

    def get_majority_class(self):
        cnts = {}
        for label in self._y_sample.unique():
            cnt = list(self._y_sample).count(label)
            cnts[cnt] = label
        return cnts[max(cnts)]

    def fit(self, X, y):
        self._y_sample = y
        self.majority_class = self.get_majority_class()
        
    def predict(self, X):
        return [self.majority_class] * X.shape[0]

    def get_params(self, deep=False):
        return {}
    
