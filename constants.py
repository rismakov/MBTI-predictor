FEATURIZED_PATH = '../MBTI_project/data/featurized_data'
TFIDF_DATA_PATH = '../MBTI_project/data/vectorized_data.csv'

TEXT_COL = 'posts'
LABEL_COL = 'type'

ENNEAGRAM_TERMS = ['1w2', '4w3', '4w5', '6w5', '7w6', 'so', 'sp', 'sx', 'enneagram', 'socionics', 'tritype']

FUNCTIONS = ['fe', 'fi', 'ne', 'ni', 'se', 'si', 'te', 'ti', 'sj', 'dom', 'sensing', 'perceiving']

IMAGE_TERMS = ['gif', 'giphy', 'image', 'img', 'imgur', 'jpeg', 'jpg', 'JPG', 'photobucket', 'png', 'tinypic']

INVALID_WORDS = ['im', 'mbti', 'functions', 'myers', 'briggs', 'types', 'type', 'personality']

MBTI_PARTS = ['nt', 'nf', 'st', 'sf', 'nts', 'nfs']

MBTI_TYPES_UPPER = [
    'ENTP', 'INTP', 'ENTJ', 'INTJ', 'ENFP', 'INFP', 'ENFJ', 'INFJ',
    'ESTP', 'ISTP', 'ESTJ', 'ISTJ', 'ESFP', 'ISFP', 'ESFJ', 'ISFJ'
]

MBTI_TYPES_LOWER = [
    'entp', 'intp', 'entj', 'intj', 'enfp', 'infp', 'enfj', 'infj',
    'estp', 'istp', 'estj', 'istj', 'esfp', 'isfp', 'esfj', 'isfj'
]

MBTI_TYPES_PLURAL = [word + 's' for word in MBTI_TYPES_LOWER]

URL_TERMS = ['http', 'https', 'www', 'com', 'youtube', 'youtu', 'watch']

# combine all invalid words to remove from TFIDF vectoried matrix
WORDS_TO_REMOVE_TFIDF = (ENNEAGRAM_TERMS + FUNCTIONS + IMAGE_TERMS + INVALID_WORDS +
                         MBTI_PARTS + MBTI_TYPES_LOWER + MBTI_TYPES_PLURAL + URL_TERMS)
