from __future__ import print_function

import logging
import numpy as np
import pandas as pd
import pickle
import time

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from data_transformation.constants import STOPWORDS
from utils.constants import VECTORIZED_PATH, TEXT_COL, TFIDF_MAX_FEATURES
from utils.utils import convert_sparse_mat_to_df, open_data, save_model, save_textfile

logging.getLogger().setLevel(logging.INFO)


def add_metadata_to_tfidf_mat(matrix, metadata, features):
    df = convert_sparse_mat_to_df(matrix, features)
    return pd.concat([df, metadata], axis=1)


def vectorize_articles(corpus):
    stop_words = stopwords.words('english') + STOPWORDS
    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES, stop_words=stop_words
    )
    matrix = vectorizer.fit_transform(corpus)

    return vectorizer, matrix


def top_tfidf_features(row, features, top_n=25):
    '''Get top n TFIDF values in row. 
    
    Returns them with their corresponding feature names.
    '''
    topn_inds = np.argsort(row)[::-1][:top_n]
    top_features = [(features[i], row[i]) for i in topn_inds]
    df = pd.DataFrame(top_features, columns=['feature', 'tfidf'])
    return df


def top_mean_features(matrix, features, grp_ids=None, min_tfidf=0.1, top_n=25):
    ''' Return the top n features that on average are most important amongst documents in rows
    indentified by indices in grp_ids. 
    '''
    if grp_ids:
        D = matrix[grp_ids].toarray()
    else:
        D = matrix.toarray()

    D[D < min_tfidf] = 0
    tfidf_means = np.mean(D, axis=0)
    return top_tfidf_features(tfidf_means, features, top_n)


def top_features_by_class(matrix, y, features, min_tfidf=0.1, top_n=25):
    ''' Return a list of dfs, where each df holds top_n features and their mean tfidf value
    calculated across documents with the same class label.
    '''
    dfs = []
    labels = np.unique(y)
    for label in labels:
        ids = np.where(y == label)
        feats_df = top_mean_features(matrix, features, ids, min_tfidf=min_tfidf, top_n=top_n)
        feats_df.label = label
        dfs.append(feats_df)
    return dfs


def top_mean_features_v2(
    matrix, features, grp_ids=None, anti_ids=None, min_tfidf=0.1, top_n=25
):
    ''' Return the top n features that on average are most important amongst documents in rows
        indentified by indices in grp_ids. '''
    if grp_ids:
        D = matrix[grp_ids].toarray()
        anti_D = matrix[anti_ids].toarray()
    else:
        D = matrix.toarray()

    D[D < min_tfidf] = 0
    tfidf_means = np.mean(D, axis=0) / np.mean(anti_D, axis=0)
    return top_tfidf_features(tfidf_means, features, top_n)


def top_features_by_class_v2(matrix, y, features, min_tfidf=0.1, top_n=25):
    '''Return a list of DataFrames, where each DataFrame holds top_n features 
    and their mean tfidf value calculated across documents with the same class 
    label. 
    '''
    dfs = []
    labels = np.unique(y)
    for label in labels:
        ids = np.where(y == label)
        anti_ids = np.where(y != label)
        feats_df = top_mean_features_v2(
            matrix, 
            features, 
            grp_ids=ids, 
            anti_ids=anti_ids, 
            min_tfidf=min_tfidf, 
            top_n=top_n
        )
        feats_df.label = label
        dfs.append(feats_df)
    return dfs


def main():
    data = open_data()

    vectorizer, matrix = vectorize_articles(data[TEXT_COL])

    save_model(vectorizer, 'mbti_tfidf_{}'.format(TFIDF_MAX_FEATURES))

    features = vectorizer.get_feature_names()
    save_textfile(features)

    df = convert_sparse_mat_to_df(matrix, features)
    df.to_csv(VECTORIZED_PATH, encoding='utf-8')


if __name__ == "__main__":
    start_time = time.time()

    main()

    seconds = time.time() - start_time
    minutes = seconds / 60
    logging.info("Vectorizer took {} minutes to run".format(minutes))
