RANDOM_STATE = 18

TFIDF_MAX_FEATURES = 15000

FEATURIZED_PATH = 'data/featurized_data.csv'
VECTORIZED_PATH = 'data/vectorized_data_{}.csv'.format(TFIDF_MAX_FEATURES)

FEATURES_PATH = 'data/features_{}'.format(TFIDF_MAX_FEATURES)

MODEL_COMPARISON_TABLE_FILE = 'model_comparison_table_{}'.format(TFIDF_MAX_FEATURES)

MODEL_FILENAME = 'models/Fitted_Model_{}_' + str(TFIDF_MAX_FEATURES)

PLOTS_PATH = 'plots/plots_by_type'
FUNCTION_PLOTS_PATH = 'plots/plots_by_functions'

TEXT_COL = 'posts'
LABEL_COL = 'type'
