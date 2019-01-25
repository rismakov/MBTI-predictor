from __future__ import division, print_function

import numpy as np
import pandas as pd
import time

from multiprocessing import Pool

from stylometry_analysis import StyleFeatures
from utils.constants import FEATURIZED_PATH, LABEL_COL, TEXT_COL
from utils.utils import open_data


FEATURES_COL = 'stylometry'

num_partitions = 10  # number of partitions to split dataframe
num_cores = 4  # number of cores on your machine


def debug(data):
    '''Prints row number while iterating over DataFrame for debugging purposes.

    :data param type: Pandas DataFrame.
    '''
    stylometry_info = []
    for i, row in data.iterrows():
        print(i)
        stylometry_info += StyleFeatures(row[TEXT_COL]).get_all_featurized_features()


def add_stylometry_info(data):
    '''Adds 'stylometry' information to inputted data.

    :param data type: Pandas DataFrame.
    :returns type: Pandas DataFrame with additional 'stylometry' column.
    '''
    data['stylometry'] = data[TEXT_COL].apply(lambda x: StyleFeatures(x).get_all_featurized_features())
    return data


def parallelize_dataframe(df, func):
    print('Spliting data.')
    df_split = np.array_split(df, num_partitions)
    print('Pooling data.')
    pool = Pool(num_cores)
    print('Concatenating data.')
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    print('Joining data.')
    pool.join()
    return df


def print_percentages_of_each_type(data):
    '''Prints the percentages each label appears in the data.

    :param data type: Pandas DataFrame.
    '''
    grouped_data = data.groupby(LABEL_COL).count()[TEXT_COL]
    total = sum(grouped_data)
    percents_of_each_type = grouped_data.apply(lambda x: round(x / total * 100, 2))
    print(percents_of_each_type)


def convert_fields_to_columns(data):
    '''Converts 'stylometry' column with dictionary type into separate columns with each dict field a separate column.

    :param data type: Pandas DataFrame with 'stylometry' column available.
    :returns type: Pandas DataFrame with additional columns, dropping 'stylometry' column.
    '''
    features = data[FEATURES_COL][0]
    for feature in features:
        feature_col = [d[feature] for d in data[FEATURES_COL]]

        if all(feature_col == 0.0):
            raise Exception('Feature {} added with all zero values'.format(feature))

        data[feature] = feature_col

    return data.drop([FEATURES_COL, TEXT_COL], axis=1)


def featurize_data(debug=False):
    data = open_data()

    print_percentages_of_each_type(data)

    if debug:
        debug(data)
    else:
        data = parallelize_dataframe(data, add_stylometry_info)

    data = convert_fields_to_columns(data)
    print(data.columns)
    data.to_csv(FEATURIZED_PATH, encoding='utf-8')


if __name__ == "__main__":
    start_time = time.time()

    featurize_data()

    seconds = time.time() - start_time
    minutes = seconds / 60
    print("Featurizer took", minutes, "minutes to run")
