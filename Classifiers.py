from __future__ import division, print_function

import cPickle
import matplotlib.pyplot as plt
import numpy as np

from itertools import izip

# import plotly.plotly as py
# import plotly.graph_objs as go

from sklearn.model_selection import train_test_split
from sklearn.metrics import auc, roc_curve
from sklearn.model_selection import cross_validate, GridSearchCV

from plot_table import print_results_in_table
from scoring import get_comprehensive_scoring_types

CAPITAL_LETTERS = 'ABCDEFGFIGKLMNOPQRSTUVWXYZ'


class Classifiers(object):
    '''
    Classifier object for fitting, storing, and comparing multiple model output
    '''

    def __init__(self, classifier_list, X, y):
        self.classifiers = classifier_list
        self.classifier_names = []
        for clf in self.classifiers:
            if clf.__class__.__name__ == 'OneVsRestClassifier':
                self.classifier_names.append(''.join([letter for letter in clf.estimator.__class__.__name__  
                                             if letter in CAPITAL_LETTERS]))
            else:
                self.classifier_names.append(''.join([letter for letter in clf.__class__.__name__ 
                                             if letter in CAPITAL_LETTERS]))

        self._X_train, self._X_test, self._y_train, self._y_test = train_test_split(X, y, 
                test_size=0.30, random_state=18)

    def train(self, save_model=False):
        for clf, name in izip(self.classifiers, self.classifier_names):
            print("\n____________{}____________".format(name))
            clf.fit(self._X_train, self._y_train)

            if save_model:
                with open('Fitted_Model_{}_Style'.format(name), 'wb') as f:
                    cPickle.dump(clf, f)

    def grid_search(self, params_dict):
        for clf, params in izip(self.classifiers, params_dict):
            print("\n____________{}____________".format(clf.__class__.__name__))
            gscv = GridSearchCV(clf, params, scoring='f1_macro')
            clf = gscv.fit(self._X_train, self._y_train)
            print('Best parameters:', clf.best_params_)
            print('Best score:', clf.best_score_)
            print()

    def test(self):
        for name, clf in izip(self.classifier_names, self.classifiers):
            print("\n____________{}____________".format(name))
            predictions = clf.predict(self._X_test)

            correct_cnt = 0
            incorrect_cnt = 0
            for true_type, pred_type in izip(self._y_test, predictions):
                for i in xrange(4):
                    if true_type[i] == pred_type[i]:
                        correct_cnt += 1
                    else:
                        incorrect_cnt += 1
            
            accuracy = correct_cnt / (correct_cnt + incorrect_cnt)
            print("Accuracy: {:.3%}".format(accuracy))
            print("\n")

    def plot_roc_curve(self):
        fig, ax = plt.subplots()
        for name, clf in zip(self.classifier_names, self.classifiers):
            predict_probas = clf.predict_proba(self._X_test)[:, 1]
            fpr, tpr, thresholds = roc_curve(self._y_test, predict_probas,
                                             pos_label=1)
            roc_auc = auc(x=fpr, y=tpr)
            ax.plot(fpr, tpr, label='{} (AUC = {:.2f})'.format(name, roc_auc))

        # 45 degree line
        x_diag = np.linspace(0, 1.0, 20)
        ax.plot(x_diag, x_diag, color='grey', ls='--')
        ax.legend(loc='best')
        ax.set_ylabel('True Positive Rate', size=20)
        ax.set_xlabel('False Positive Rate', size=20)
        ax.tick_params(axis='both', which='major', labelsize=16)
        fig.set_size_inches(15, 10)
        fig.savefig('plots/ROC_curves', dpi=100)

    def print_cross_val_results(self):
        # iterate over all classifiers
        mean_cross_val_metrics = {}
        for clf, name in izip(self.classifiers, self.classifier_names):
            print('___________________{}___________________'.format(name))

            scoring = get_comprehensive_scoring_types()
            cross_val_metrics = cross_validate(clf, self._X_train, self._y_train, scoring=scoring)

            # get mean of all cross val results
            mean_cross_val_metrics[name] = {k: np.mean(v) for k, v in cross_val_metrics.iteritems() 
                    if 'test' in k}

        print_results_in_table(mean_cross_val_metrics, self.classifiers, self.classifier_names)
        
