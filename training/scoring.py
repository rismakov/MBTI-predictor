from sklearn.metrics import (accuracy_score, f1_score,
                             make_scorer, precision_score, recall_score)

from constants import LETTER_TYPES, PERSONALITY_DIMS

AVERAGE_TYPE = 'macro'


def get_multiclass_metrics(true, pred):
    '''Returns dict of all metrics (accuracy, precision, recall, and f1).

    :param true type: list or array-type of true labels.
    :param pred type: list of array-type of predicted labels.

    :returns type: dict of floats with keys: ['accuracy', 'precision', 'recall', and 'f1'].
    '''
    metrics = {}
    metrics['accuracy'] = accuracy_score(true, pred)
    metrics['precision'] = precision_score(true, pred, average=AVERAGE_TYPE)
    metrics['recall'] = recall_score(true, pred, average=AVERAGE_TYPE)
    metrics['f1'] = f1_score(true, pred, average=AVERAGE_TYPE)

    return metrics


def scorer_func_for_each_letter(
    true, pred, dim, scoring_type, average_types=['macro']
):
    '''Returns score from scoring function given personality dimension and scoring type.
    '''
    metrics = {}
    for i, dim in enumerate(PERSONALITY_DIMS):
        true_dim = [x[i]for x in true]
        pred_dim = [x[i]for x in pred]

        metrics[dim] = get_multiclass_metrics(true_dim, pred_dim)

    return metrics[dim][scoring_type]


def get_metrics_for_letter_type(scoring, dim, letter_type):
    '''Iterates through every scoring_type to grab result from scoring function.
    '''
    scoring_types = ['accuracy', 'precision', 'recall', 'f1']

    for scoring_type in scoring_types:
        key_name = letter_type + '_' + scoring_type
        scoring[key_name] = make_scorer(
            scorer_func_for_each_letter, dim=dim, scoring_type=scoring_type, greater_is_better=True
        )

    return scoring


def get_comprehensive_scoring_types():
    '''Iterates through every MBTI Personality dimension to grab result from scoring function.
    '''
    scoring = {
        'accuracy': make_scorer(accuracy_score),
        'precision': make_scorer(precision_score, average=AVERAGE_TYPE),
        'recall': make_scorer(recall_score, average=AVERAGE_TYPE),
        'f1': make_scorer(f1_score, average=AVERAGE_TYPE),
    }

    # add metrics for each letter type (i.e. E-I, N-S, F-T, J-P) to full type metrics
    for dim, letter_type in zip(PERSONALITY_DIMS, LETTER_TYPES):
        scoring = get_metrics_for_letter_type(scoring, dim, letter_type)

    return scoring
