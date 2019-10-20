from __future__ import division

import numpy as np
import pandas as pd
import pickle
import scipy
import zipfile

from constants import FEATURES_PATH, FEATURIZED_PATH, VECTORIZED_PATH

ZIP_FILENAME = 'data/mbti_1.csv.zip'
FILENAME = 'mbti_1.csv'


def open_data():
    '''Opens MBTI text data with columns 'type' and 'posts'.

    :returns type: Pandas DataFrame.
    '''
    zf = zipfile.ZipFile(ZIP_FILENAME)
    return pd.read_csv(zf.open(FILENAME), encoding='utf-8')


def open_textfile():
    with open(FEATURES_PATH) as f:
        return [word.replace('\n', '') for word in f.readlines()]


def open_concat_data(filename1, filename2):
    '''Opens featurized and vectorized data and returns concatenated merged data.
    '''
    data_1 = pd.read_csv(filename1, encoding='utf-8').drop(['Unnamed: 0'], axis=1)
    data_2 = pd.read_csv(filename2, encoding='utf-8').drop(['Unnamed: 0'], axis=1)

    return pd.concat([data_1, data_2], axis=1)


def open_model(filename):
    return pickle.load(open(filename, 'rb'))


def save_textfile(my_list):
    with open(FEATURES_PATH, 'w') as f:
        for item in my_list:
            f.write('{}\n'.format(item))


def save_model(model, filename):
    with open(filename, 'wb') as f:
        pickle.dump(model, f)

def convert_sparse_mat_to_df(matrix, columns):
    return pd.DataFrame(matrix.toarray(), columns=columns)


def convert_df_to_sparse_mat(df):
    return scipy.sparse.csr_matrix(df.values)


def get_key_of_dict_by_value(my_dict, value):
    '''Returns the key of a dictionary by a specified value.

    :param type my_dict: dict.
    :param type value: value that exists inside my_dict.
    '''
    return list(my_dict.keys())[list(my_dict.values()).index(value)]


def get_label_percentages(data, label_col):
    '''Return the distribution of all label classes within the data.

    Parameters:
        data : pandas.DataFrame
            Data to get counts of.
        label_col : str
            Column by which to group by.

    Returns:
        pandas.DataFrame
            Returns DataFrame with `label_col` unique values as index and the
            percentage the label appears in the data as values. 
    '''
    grouped_data = data.groupby(label_col).count()

    # take any column - as all are counts
    counts = grouped_data[grouped_data.columns[0]]
    total = counts.sum()
    
    return counts.apply(lambda x: x / total * 100)


def get_freq_of_characters_in_text_in_list(lst, search_items, normalizer):
    '''Calculates the combined frequency given strings of characters within a list appear in a list of text.

    Example:
        lst = ['apple.gif', 'apple', '.gif', 'png']
        search_items = ['gif', 'apple']
        normalizer = 4

        returns: Float(3/4)

    :param lst: List of items to search through.
    :param search_items: List of items you want the combined count of.
    :param normalizer: Integer by which to normalize count.

    :returns type: Float.
    '''

    cnts = (any(search_item in lst_item for search_item in search_items) for lst_item in lst)

    return sum(cnts) / normalizer


def get_freq_of_items_in_list(lst, search_items, normalizer):
    '''Calculates the combined frequency of each item within a specified list divided by the normalizer specified.

    Example:
        lst = ['apple.gif', 'apple', '.gif']
        search_items = ['.gif', 'apple']
        normalizer = 3

        returns: Float(2/3)

    :param lst: List of items to search through.
    :param search_items: List of items you want the combined count of.
    :param normalizer: Integer by which to normalize count.

    :returns type: Float.
    '''
    cnts = [lst.count(item) for item in search_items]

    return sum(cnts) / normalizer


def get_count_of_characters_in_text(text, characters):
    '''Gets the count of a specific word or string of characters within a block of text.

    :param text: String of text which to search through.
    :param characters: String of characters which to count.

    :returns type: Int.
    '''
    return len(text.split(characters)) - 1
    :param target_column type: str. the column containing the values to split and explode.
    :param separator type: str. the character on which to split.
    '''
    row_accumulator = []
    def split_list_to_rows(row, separator):
        split_row = row[target_column].split(separator)
        for s in split_row:
            new_row = row.to_dict()
            new_row[target_column] = s
            row_accumulator.append(new_row)

    df.apply(split_list_to_rows, axis=1, args=(separator, ))
    exploded_df = pd.DataFrame(row_accumulator)
    return exploded_df


def get_top_inds(my_list, top_n=10):
    sorted_inds = np.argsort(my_list)[::-1]
    return sorted_inds[:top_n]


def remove_negative_values(df):
    '''Scales data to convert negative values in columns where they exist to positive values.
    NOTE: makes assumption that columns with negative values are at minimum -1 ('polarity' is expected to be the only negative column).

    :param df type: Pandas DataFrame.
    :returns type: Pandas DataFrame with negative values converted to positive values.
    '''
    columns_where_neg_values_exist = df.columns[(df < 0).any()]
    logging.info('Removing negative values from columns : {}'.format(
        columns_where_neg_values_exist)
    )

    for col in columns_where_neg_values_exist:
        df[col] = df[col] + 1

    return df

def sort_dict_values(d, key_order):
    return [d[key] for key in key_order]