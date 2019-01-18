from sklearn.metrics import (accuracy_score, f1_score,
                             make_scorer, precision_score, recall_score)

from constants import LETTER_TYPES, PERSONALITY_DIMS


def get_precision_recall_f1(true, pred, average_type):
    metrics = {}
    metrics['precision'] = precision_score(true, pred, average=average_type)
    metrics['recall'] = recall_score(true, pred, average=average_type)
    metrics['f1'] = f1_score(true, pred, average=average_type)
    return metrics


def get_multiclass_metrics(true, pred, average_types):
    metrics = {}
    metrics['accuracy'] = accuracy_score(true, pred)

    for average_type in average_types:
        metrics[average_type] = get_precision_recall_f1(true, pred, average_type)

    return metrics


def get_metrics_for_each_letter(
    true, pred, return_dim=None, first_level=None, second_level=None, average_types=['macro']
):
    metrics = {}
    for i, dim in enumerate(PERSONALITY_DIMS):
        true_dim = [x[i]for x in true]
        pred_dim = [x[i]for x in pred]

        metrics[dim] = get_multiclass_metrics(true_dim, pred_dim, average_types=average_types)

    if return_dim and first_level and second_level:
        return metrics[return_dim][first_level][second_level]
    elif return_dim and first_level:
        return metrics[return_dim][first_level]
    else:
        return metrics


def get_metrics_for_letter_type(scoring, dim, letter_type):
    scoring_types = ['accuracy', 'precision', 'recall', 'f1']
    first_levels = ['accuracy', 'macro', 'macro', 'macro']
    second_levels = [None, 'precision', 'recall', 'f1']

    for scoring_type, first_level, second_level in zip(scoring_types, first_levels, second_levels):
        scoring[letter_type + '_' + scoring_type] = make_scorer(get_metrics_for_each_letter, return_dim=dim, 
                                                                first_level=first_level, second_level=second_level, 
                                                                greater_is_better=True)

    return scoring


def get_comprehensive_scoring_types():
    scoring = {
        'accuracy': make_scorer(accuracy_score), 
        'precision': make_scorer(precision_score, average='macro'), 
        'recall': make_scorer(recall_score, average='macro'),
        'f1': make_scorer(f1_score, average='macro'),
    }

    # get metrics for each letter type (i.e. E-I, N-S, F-T, J-P)
    for dim, letter_type in zip(PERSONALITY_DIMS, LETTER_TYPES):
        scoring = get_metrics_for_letter_type(scoring, dim, letter_type)

    return scoring
