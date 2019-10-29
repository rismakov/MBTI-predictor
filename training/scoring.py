from sklearn.metrics import (
    accuracy_score, f1_score, make_scorer, precision_score, recall_score
)

from constants import LETTER_TYPES, PERSONALITY_DIMS
from utils.constants import FUNCTION_INDS

AVERAGE_TYPE = 'macro'


def get_scores_for_all_dimensions(true, pred):
    """Get dict with metrics information for all function types.

    Adds full MBTI type metrics as well as metrics for each indivdual MBTI 
    dimension (i.e. E-I, N-S, etc.). This is defined in `FUNCTION_INDS`.

    Parameters
    ----------
    true : list or array
        True labels.
    pred : list or array
        Predicted labels.

    Returns
    -------
    Dict[str, Dict[str, float]]
        Returns dict with keys as the MBTI dimension (i.e. full MBTI, E-I, N-S, 
        etc.) and values as the metrics.
    """
    scores = {}
    for description, (start_ind, end_ind) in FUNCTION_INDS.items():
        true_set = [x[start_ind:end_ind] for x in true] 
        pred_set = [x[start_ind:end_ind] for x in pred]

        scores[description] = get_multiclass_metrics(true_set, pred_set)
    
    return scores


def get_multiclass_metrics(true, pred):
    '''Get dict with metrics information (accuracy, precision, recall, and f1).

    Parameters
    ----------
    true : list or array 
        True labels.
    pred : list or array
        Predicted labels.

    Returns
    -------
    Dict[str, float] 
        Returns dict with keys ('accuracy', 'precision', 'recall', 'f1').
    '''
    return {
        'accuracy': accuracy_score(true, pred),
        'precision': precision_score(true, pred, average=AVERAGE_TYPE),
        'recall': recall_score(true, pred, average=AVERAGE_TYPE),
        'f1': f1_score(true, pred, average=AVERAGE_TYPE),
    }