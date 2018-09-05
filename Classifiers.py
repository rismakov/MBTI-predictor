from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import (recall_score, precision_score, f1_score, 
                             accuracy_score, confusion_matrix, roc_curve, auc, roc_auc_score, make_scorer)
from itertools import izip
from sklearn.model_selection import GridSearchCV, cross_val_score, KFold, cross_validate
from scipy.stats import hmean
import cPickle

from numpy.random import choice

from BaselineClassifier import BaselineClassifier

from scoring import get_metrics_for_each_letter

from collections import OrderedDict

import plotly.plotly as py
import plotly.graph_objs as go


personality_dims = [
        'Extraversion-Introversion', 
        'Intuition-Sensing', 
        'Feeling-Thinking', 
        'Judging-Perceiving'
    ]

letter_types = ['E_I', 'N_S', 'F_T', 'J_P']

capital_letters = 'ABCDEFGFIGKLMNOPQRSTUVWXYZ'

class Classifiers(object):
    '''
    Classifier object for fitting, storing, and comparing multiple model output
    '''

    def __init__(self, classifier_list, X, y):
        self.classifiers = classifier_list
        self.classifier_names = []
        for clf in self.classifiers:
            if clf.__class__.__name__  == 'OneVsRestClassifier':
                self.classifier_names.append(''.join([letter for letter in clf.estimator.__class__.__name__  
                                             if letter in capital_letters]))
            else:
                self.classifier_names.append(''.join([letter for letter in clf.__class__.__name__ 
                                             if letter in capital_letters]))

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
            
            accuracy_score = correct_cnt / (correct_cnt + incorrect_cnt)
            print("Accuracy: {:.3%}".format(accuracy_score))
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


    def print_results_in_table(self, metrics):
        fig, ax = plt.subplots()

        all_ordered_keys = []
        for letter_type in [''] + [letter + '_' for letter in letter_types]:
            for scoring_type in ['accuracy', 'precision', 'recall', 'f1']:
                all_ordered_keys.append('test_' + letter_type + scoring_type)

        scoring_types = all_ordered_keys

        # metrics [clf name] [scoring type]
        cell_text = [['{:.2f}'.format(metrics[clf_name][scoring_type] * 100.0) 
            for clf_name in self.classifier_names] for scoring_type in scoring_types]

        # Get some pastel shades for the colors
        colors = [
            'salmon', 'salmon', 'salmon', 'salmon',
            'mediumaquamarine', 'mediumaquamarine', 'mediumaquamarine', 'mediumaquamarine',
            'orange', 'orange', 'orange', 'orange',
            'skyblue', 'skyblue', 'skyblue', 'skyblue',
            'silver', 'silver', 'silver', 'silver'
        ]

        color_increase = {
            'salmon': 'orangered',
            'mediumaquamarine': 'teal',
            'orange': 'chocolate',
            'skyblue': 'deepskyblue',
            'silver': 'gray'
        }
        
        cell_colors = [[color] * len(self.classifiers) for color in colors]

        cell_text_ints = [[float(x) for x in lst] for lst in cell_text]
        max_clf_inds = [lst.index(max(lst)) for lst in cell_text_ints]
        for metric_ind, clf_ind in enumerate(max_clf_inds):
            current_color = cell_colors[metric_ind][clf_ind]
            cell_colors[metric_ind][clf_ind] = color_increase[current_color]

        # ax.axis('tight')
        ax.axis('off')
        table = ax.table(
            cellText=cell_text, cellColours=cell_colors,
            # cellColours=None,
            # cellLoc='right', colWidths=None,
            rowLabels=scoring_types, rowColours=colors, rowLoc='left',
            colLabels=self.classifier_names, # colColours=None, colLoc='center',
            loc='center'
        )
        
        table.set_fontsize(14)
        # table.scale(1.5, 3.0)

        # plt.title('Baseline Results')
        # fig.tight_layout()

        fig.savefig('table', dpi=100)
        plt.show()
        plt.close()


    def get_metrics_for_letter_type(self, scoring, dim, letter_type):
        scoring[letter_type + '_' + 'accuracy'] = make_scorer(get_metrics_for_each_letter, 
            return_dim=dim, first_level='accuracy', greater_is_better=True)
        scoring[letter_type + '_' + 'precision'] = make_scorer(get_metrics_for_each_letter, 
            return_dim=dim, first_level='macro', second_level= 'precision', greater_is_better=True)
        scoring[letter_type + '_' + 'recall'] =make_scorer(get_metrics_for_each_letter, 
            return_dim=dim, first_level='macro', second_level= 'recall', greater_is_better=True)
        scoring[letter_type + '_' + 'f1'] =make_scorer(get_metrics_for_each_letter, 
            return_dim=dim, first_level='macro', second_level= 'f1', greater_is_better=True)

        return scoring

    def print_cross_val_results(self):
        all_metrics = {}
        all_binary_metrics = {}

        # iterate over all classifiers
        mean_cross_val_metrics = {}
        for clf, name in izip(self.classifiers, self.classifier_names):
            print('___________________{}___________________'.format(name))

            scoring = {
                'accuracy': make_scorer(accuracy_score), 
                'precision': make_scorer(precision_score, average='macro'), 
                'recall': make_scorer(recall_score, average='macro'),
                'f1': make_scorer(f1_score, average='macro'),
            }

            # get metrics for each letter type (i.e. E-I, N-S, F-T, J-P)
            for dim, letter_type in zip(personality_dims, letter_types):
                scoring = self.get_metrics_for_letter_type(scoring, dim, letter_type)
            
            cross_val_metrics = cross_validate(clf, self._X_train, self._y_train, scoring=scoring)

            # get mean of all cross val results
            mean_cross_val_metrics[name] = {k: np.mean(v) for k, v in cross_val_metrics.iteritems() 
                if 'test' in k}

        self.print_results_in_table(mean_cross_val_metrics)
        
