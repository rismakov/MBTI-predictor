from scipy.stats import hmean

from training.scoring import (
    get_multiclass_metrics, get_scores_for_all_dimensions
)

TRUE = ['ENTP', 'INFJ', 'ENTP', 'ENTP'] 
PRED = ['ENTP', 'INFJ', 'INFJ', 'ENTP']

def get_full_mbti_expected_metrics():
    entp_precision = 1 
    infj_precision = 1 / 2  
    entp_recall = 2 / 3
    infj_recall = 1
    entp_f1 = hmean([entp_precision, entp_recall])
    infj_f1 = hmean([infj_precision, infj_recall])

    expected = {
        'accuracy': 3/4,
        'precision': (entp_precision + infj_precision) / 2,
        'recall': (entp_recall + infj_recall) / 2,
        'f1': (entp_f1 + infj_f1) / 2,
    }
    actual = get_multiclass_metrics(TRUE, PRED)

    return expected, actual

def get_NS_expected_metrics():
    true = ['N', 'N', 'N', 'N'] 
    pred = ['N', 'N', 'N', 'N']
    
    expected = {
        'accuracy': 1,
        'precision': 1,
        'recall': 1,
        'f1': 1,
    }
    actual = get_multiclass_metrics(true, pred)

    return expected, actual

def test_get_scores_for_all_dimensions():
    full_expected, full_actual = get_full_mbti_expected_metrics()
    assert full_expected == full_actual

    NS_expected, NS_actual = get_NS_expected_metrics()
    assert NS_expected == NS_actual

    expected = {
        'MBTI': full_expected,
        'Extraversion-Introversion': full_expected,
        'Intuition-Sensing': NS_expected,
        'Feeling-Thinking': full_expected,
        'Judging-Perceiving': full_expected,
    }

    actual = get_scores_for_all_dimensions(TRUE, PRED)
    
    assert expected == actual