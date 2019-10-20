from collections import OrderedDict

from utils.constants import MBTI_TYPES

FUNCTION_MAPPINGS = {
    'EN': 'Extraversion-Intuition',
    'ES': 'Extraversion-Sensing',
    'IN': 'Introversion-Intuition',
    'IS': 'Introversion-Sensing',
    'E': 'Extraversion',
    'I': 'Introversion',
    'N': 'Intuition',
    'S': 'Sensing',
    'T': 'Thinking',
    'F': 'Feeling',
    'J': 'Judging',
    'P': 'Perceiving'
}

FUNCTION_INDS = {
    'MBTI': (0, 4),
    'Extraversion-Introversion': (0, 1),
    'Intuition-Sensing': (1, 2),
    'Feeling-Thinking': (2, 3),
    'Judging-Perceiving': (3, 4),
    'Temperment': (1, 3),
}

LETTERS = ['E', 'I', 'N', 'S', 'F', 'T', 'J', 'P']

FUNCTION_PAIRS = [('E', 'I'), ('N', 'S'), ('F', 'T'), ('J', 'P')]

GLOBAL_PERCENTAGES = OrderedDict([
    ('ENFJ', 2.5),
    ('ENFP', 8.1),
    ('ENTJ', 1.8),
    ('ENTP', 3.2),
    ('INFJ', 1.5),
    ('INTJ', 2.1),
    ('INFP', 4.4),
    ('INTP', 3.3),
    ('ESFJ', 12.3),
    ('ESFP', 8.5),
    ('ESTJ', 8.7),
    ('ESTP', 4.3),
    ('ISFJ', 13.8),
    ('ISFP', 8.8),
    ('ISTJ', 11.6),
    ('ISTP', 5.4),
])
