from __future__ import division

import pandas as pd
import zipfile

ZIP_FILENAME = '../MBTI_project/data/mbti_1.csv.zip'
FILENAME = 'mbti_1.csv'


def open_data():
    '''Opens MBTI text data with columns 'type' and 'posts'.

    :returns type: Pandas DataFrame.
    '''
    zf = zipfile.ZipFile(ZIP_FILENAME)
    return pd.read_csv(zf.open(FILENAME), encoding='utf-8')


def get_freq_of_items_in_list(lst, search_items, normalizer):
    '''Counts the combined frequency of each item within a specified list divided by the length of the normalizer
    specified.

    :param lst: List of items to search through.
    :param search_items: List of items you want the combined count of.
    :param normalizer: Integer by which to normalize count.

    :returns type: Float.
    '''
    cnts = [lst.count(item) for item in search_items]

    return sum(cnts) / normalizer


def get_count_of_characters_in_text(text, characters):
    '''Gets the count of a specific word or string of characters within a block of text.

    :param text: String which to search through.
    :param characters: String of characters which to count.

    :returns type: Int.
    '''
    return len(text.split(characters)) - 1
