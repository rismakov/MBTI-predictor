RANDOM_STATE = 18

TFIDF_MAX_FEATURES = 15000

FEATURIZED_PATH = 'data/featurized_data.csv'
VECTORIZED_PATH = 'data/vectorized_data_{}.csv'.format(TFIDF_MAX_FEATURES)

FEATURES_PATH = 'data/features_{}'.format(TFIDF_MAX_FEATURES)

MODEL_COMPARISON_TABLE_FILE = 'model_comparison_table_{}'.format(TFIDF_MAX_FEATURES)

PLOTS_PATH = 'plots/plots_by_type'
FUNCTION_PLOTS_PATH = 'plots/plots_by_functions'

TEXT_COL = 'posts'
LABEL_COL = 'type'

ENNEAGRAM_TERMS = [
  '1w2', '2w1', '2w3', '3w2', '3w4', '4w3', '4w5',
  '6w5', '6w7', '7w6', '7w8', '8w7', '8w9', '9w8',
  'so', 'sp', 'sx', 'enneagram', 'ennegram', 'socionics', 'tritype',
  '7s', '8s'
]

FUNCTIONS = ['fe', 'fi', 'ne', 'ni', 'se', 'si', 'te', 'ti', 'sj', 'dom', 'sensing', 'perceiving']

IMAGE_TERMS = ['gif', 'giphy', 'image', 'img', 'imgur', 'jpeg', 'jpg', 'JPG', 'photobucket', 'php', 'png', 'tinypic']

INVALID_WORDS = [
  'im', 'mbti', 'functions', 'myers', 'briggs', 'types', 'type',
  'personality', '16personalities', '16', 'personalitycafe', 'tapatalk'
]

MBTI_PARTS = [
  'es', 'fj', 'nt', 'nf', 'st', 'sf', 'sj',
  'nts', 'nfs', 'sts', 'sfs', 'sjs',
  'enxp', 'exfj', 'exfp', 'esxp',
  'ixfp', 'ixtp', 'ixtj', 'ixfj',
  'xntp', 'xnfj',
  'nfp', 'ntp', 'ntj', 'nfp', 'sfj',
]

MBTI_TYPES_UPPER = [
  'ENFJ', 'ENFP', 'ENTJ', 'ENTP',
  'ESFJ', 'ESFP', 'ESTJ', 'ESTP',
  'INFJ', 'INFP', 'INTJ', 'INTP',
  'ISFJ', 'ISFP', 'ISTJ', 'ISTP'
]

MBTI_TYPES_LOWER = [mbti_type.lower() for mbti_type in MBTI_TYPES_UPPER]

MBTI_TYPES_PLURAL = [word + 's' for word in MBTI_TYPES_LOWER]

URL_TERMS = ['http', 'https', 'www', 'com', 'youtube', 'youtu', 'watch']

# combine all invalid words to remove from TFIDF vectoried matrix
WORDS_TO_REMOVE_TFIDF = (ENNEAGRAM_TERMS + FUNCTIONS + IMAGE_TERMS + INVALID_WORDS +
                         MBTI_PARTS + MBTI_TYPES_LOWER + MBTI_TYPES_PLURAL + URL_TERMS)
