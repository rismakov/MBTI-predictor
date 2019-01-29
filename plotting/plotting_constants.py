from utils.constants import MBTI_TYPES_UPPER

GLOBAL_PERCENTAGES = {
    'ISFJ': 13.8,
    'ESFJ': 12.3,
    'ISTJ': 11.6,
    'ISFP': 8.8,
    'ESTJ': 8.7,
    'ESFP': 8.5,
    'ENFP': 8.1,
    'ISTP': 5.4,
    'INFP': 4.4,
    'ESTP': 4.3,
    'INTP': 3.3,
    'ENTP': 3.2,
    'ENFJ': 2.5,
    'INTJ': 2.1,
    'ENTJ': 1.8,
    'INFJ': 1.5
}

COLOR_MAPPINGS = {
    'EN': 'dodgerblue',
    'ES': 'slategray',
    'IN': 'lightseagreen',
    'IS': 'salmon',
}

PLOT_COLORS = [COLOR_MAPPINGS[mbti_type[:2]] for mbti_type in MBTI_TYPES_UPPER]

FUNCTION_LETTERS = ['E', 'I', 'N', 'S', 'F', 'T', 'J', 'P']

LETTER_COLOR_MAPPINGS = {
    'E': 'darkolivegreen',
    'I': 'darkolivegreen',
    'N': 'black',
    'S': 'black',
    'F': 'indianred',
    'T': 'indianred',
    'J': 'darkgray',
    'P': 'darkgray',
}

LETTER_PLOT_COLORS = [LETTER_COLOR_MAPPINGS[letter] for letter in FUNCTION_LETTERS]
