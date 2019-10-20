from collections import OrderedDict

from plotting.plotting import (
    get_distribution_diff, 
    get_letter_percents_from_type_percents
)

def test_get_distribution_diff():
    dist_1 = OrderedDict([
        ('ENFJ', 2.1), 
        ('ENFP', 7.7), 
        ('ENTJ', 2.6), 
        ('ENTP', 7.8), 
    ])
    
    dist_2 = OrderedDict([
        ('ENFJ', 2.5), 
        ('ENFP', 8.1), 
        ('ENTJ', 1.8), 
        ('ENTP', 3.2), 
    ])

    expected = OrderedDict([
        ('ENFJ', -0.4), 
        ('ENFP', -0.4), 
        ('ENTJ', 0.8), 
        ('ENTP', 4.6), 
    ])

    actual = get_distribution_diff(dist_1, dist_2)

    assert expected.keys() == actual.keys()
    assert expected.values() == actual.values()


def test_get_letter_percents_from_type_percents():
    ENFJ_percent = 2.19
    ENTP_percent = 7.78
    INTJ_percent = 2.66
    ESTP_percent = 7.89

    dataset_percents = OrderedDict([
        ('ENFJ', ENFJ_percent), 
        ('ENTP', ENTP_percent), 
        ('INTJ', INTJ_percent), 
        ('ESTP', ESTP_percent),
    ])

    expected = OrderedDict([
        ('E', ENFJ_percent + ENTP_percent + ESTP_percent),
        ('I', INTJ_percent),
        ('N', ENFJ_percent + ENTP_percent + INTJ_percent),
        ('S', ESTP_percent),
        ('F', ENFJ_percent),
        ('T', ENTP_percent + INTJ_percent + ESTP_percent),
        ('J', ENFJ_percent + INTJ_percent),
        ('P', ENTP_percent + ESTP_percent),
    ])

    actual = get_letter_percents_from_type_percents(dataset_percents)

    assert actual.keys() == expected.keys()
    assert actual.values() == expected.values()
