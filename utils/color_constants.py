from collections import OrderedDict

from utils.constants import LABELS

# ----------------------------------
# model comparison table -----------
# ----------------------------------

colors = [
    'salmon', 
    'mediumaquamarine',
    'orange',
    'skyblue', 
    'silver',
]

TABLE_COLORS = []
for color in colors:
    TABLE_COLORS += [color] * 4

COLOR_INCREASE = {
    'salmon': 'orangered',
    'mediumaquamarine': 'teal',
    'orange': 'chocolate',
    'skyblue': 'dodgerblue',
    'silver': 'gray'
}

# ----------------------------------
# writing style comparison plots ---
# ----------------------------------

FACECOLOR = 'white'  # '#F0F0F0'

COLOR_MAPPINGS = {
    'EN': 'dodgerblue',
    'ES': 'slategray',
    'IN': 'lightseagreen',
    'IS': 'salmon',
}

PLOT_COLORS = [COLOR_MAPPINGS[mbti_type[:2]] for mbti_type in LABELS]

LETTER_COLOR_MAPPINGS = OrderedDict([
    ('E', 'skyblue'),
    ('I', 'skyblue'),
    ('N', 'black'),
    ('S', 'black'),
    ('F', 'indianred'),
    ('T', 'indianred'),
    ('J', 'darkgray'),
    ('P', 'darkgray'),
])

LETTER_PLOT_COLORS = LETTER_COLOR_MAPPINGS.values()
