from __future__ import division, print_function

import logging
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sn

from sklearn.model_selection import train_test_split
from sklearn.metrics import auc, confusion_matrix, roc_curve
from sklearn.model_selection import cross_validate, GridSearchCV

from constants import RANDOM_STATE
from metrics_table import print_results_in_table
from plotting.plotting_constants import FUNCTION_INDS
from plotting.plotting_utils import plot_table, save_fig
from scoring import get_comprehensive_scoring_types
from utils.constants import MBTI_TYPES, MODEL_FILENAME
from utils.utils import save_model


class Classifiers(object):
    '''Classifier object for fitting and comparing multiple model output.'''

    def __init__(self, classifier_list, X, y):
        self.classifiers = classifier_list
        self.classifier_names = [
            self.get_abbr_class_name(clf) for clf in self.classifiers
        ]

        self._X_train, self._X_test, self._y_train, self._y_test = (
            train_test_split(X, y, test_size=0.30, random_state=RANDOM_STATE)
        )

        logging.info('{} labels in training set.'.format(len(self._y_train)))
        logging.info('{} lables in test set'.format(len(self._y_test)))

    def get_abbr_class_name(self, clf):
        '''Returns an abbreviated version of the classifier name. 
        
        Example: Random Forest returns `RF`.
        '''
        clf_name = clf.__class__.__name__
        if clf_name == 'OneVsRestClassifier':
            clf_name = clf.estimator.__class__.__name__

        return ''.join(
            [letter for letter in clf_name if letter == letter.upper()]
        )

    def fit(self):
        for clf, name in zip(self.classifiers, self.classifier_names):
            print("\n______________{}______________".format(name))
            clf.fit(self._X_train, self._y_train)

            save_model(clf, MODEL_FILENAME.format(name))

    def grid_search(self, params_dict):
        for clf, params in zip(self.classifiers, params_dict):
            print("\n______________{}______________".format(
                clf.estimator.__class__.__name__)
            )
            gscv = GridSearchCV(clf, params, scoring='f1_macro')
            clf = gscv.fit(self._X_train, self._y_train)
            print('Best parameters:', clf.best_params_)
            print('Best score:', clf.best_score_)
            print()

    def test_all_clfs(self):
        for name, clf in zip(self.classifier_names, self.classifiers):
            print("\n______________{}______________".format(name))
            predictions = clf.predict(self._X_test)

            correct_cnt = 0
            incorrect_cnt = 0
            for true_type, pred_type in zip(self._y_test, predictions):
                for i in range(4):
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

    def print_cross_val_results(self, filename):
        # iterate over all classifiers
        mean_cross_val_metrics = {}
        for clf, name in zip(self.classifiers, self.classifier_names):
            print('___________________{}___________________'.format(name))

            scoring = get_comprehensive_scoring_types()
            cross_val_metrics = cross_validate(
                clf, self._X_train, self._y_train, scoring=scoring
            )

            # get mean of all cross val results
            mean_cross_val_metrics[name] = {
                k: np.mean(v) for k, v in cross_val_metrics.items() if 'test' in k
            }

        print_results_in_table(
            mean_cross_val_metrics, 
            self.classifiers, 
            self.classifier_names, 
            filename=filename
        )
    
    def plot_test_results():
        num_clfs = len(self.classifiers)
        for i, name, clf in zip(
            range(num_clfs), self.classifier_names, self.classifiers
        ):
            plt.plot(i)
        


    def get_cm(self):
        cms = {}
        for name, clf in zip(self.classifier_names, self.classifiers):
            predicted = clf.predict(self._X_test)

            for description, inds in FUNCTION_INDS.items():
                start_ind, end_ind = inds
                true = [x[start_ind:end_ind]for x in self._y_test]
                pred = [x[start_ind:end_ind]for x in predicted]
            
                cm = confusion_matrix(true, pred)  # labels=MBTI_TYPES
                cm_percentage =  [x / sum(x) for x in cm]
                # plt.imshow(cm, cmap='binary')
            
                #  sn.set(font_scale=1.4)  # for label size
                plt.figure(figsize = (10,7))
                sn.heatmap(cm, annot=True, fmt='d')  # , xticklabels=, yticklabels=)
                plt.title(description)
                plt.show()

                plt.figure(figsize = (10,7))
                sn.heatmap(cm_percentage, annot=True, annot_kws={"size": 10})  # , xticklabels=, yticklabels=)
                plt.title(description)
                plt.show()

        return cms
