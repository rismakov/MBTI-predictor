RANDOM_STATE = 18

FEATURIZED_PATH = 'data/featurized_data.csv'

TFIDF_MAX_FEATURES = 10000
VECTORIZED_PATH = 'data/vectorized_data_{}.csv'.format(TFIDF_MAX_FEATURES)
FEATURES_PATH = 'data/features_{}'.format(TFIDF_MAX_FEATURES)

MODEL_FILENAME = 'models/Fitted_Model_{}_' + str(TFIDF_MAX_FEATURES)

PLOTS_PATH = 'plots/plots_by_type'
FUNCTION_PLOTS_PATH = 'plots/plots_by_functions'

TEXT_COL = 'posts'
LABEL_COL = 'type'

LABELS = [
  'ENFJ', 
  'ENFP', 
  'ENTJ', 
  'ENTP',
  'ESFJ', 
  'ESFP', 
  'ESTJ', 
  'ESTP',
  'INFJ', 
  'INFP', 
  'INTJ', 
  'INTP',
  'ISFJ', 
  'ISFP', 
  'ISTJ', 
  'ISTP'
]

LABELS_LOWER = [mbti_type.lower() for mbti_type in LABELS]

LABELS_PLURAL = [word + 's' for word in LABELS_LOWER]
