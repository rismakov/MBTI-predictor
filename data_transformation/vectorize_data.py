from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from constants import LABEL_COL, TEXT_COL, VECTORIZED_PATH, WORDS_TO_REMOVE_TFIDF
from utils import open_data


def add_metadata_to_tfidf_mat(matrix, metadata, vectorizer):
    df = pd.DataFrame(matrix.toarray(), columns=vectorizer.get_feature_names())
    return pd.concat([df, metadata], axis=1)


def vectorize_articles(corpus):
    stop_words = stopwords.words('english') + WORDS_TO_REMOVE_TFIDF
    vectorizer = TfidfVectorizer(max_features=1000, stop_words=stop_words)
    matrix = vectorizer.fit_transform(corpus)

    return vectorizer, matrix


def top_tfidf_features(row, features, top_n=25):
    ''' Get top n tfidf values in row and return them with their corresponding feature names.'''
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_features = [(features[i], row[i]) for i in topn_ids]
    print(top_features)
    df = pd.DataFrame(top_features)
    df.columns = ['feature', 'tfidf']
    return df


def top_mean_features(matrix, features, grp_ids=None, min_tfidf=0.1, top_n=25):
    ''' Return the top n features that on average are most important amongst documents in rows
        indentified by indices in grp_ids. '''
    if grp_ids:
        D = matrix[grp_ids].toarray()
    else:
        D = matrix.toarray()

    D[D < min_tfidf] = 0
    tfidf_means = np.mean(D, axis=0)
    return top_tfidf_features(tfidf_means, features, top_n)


def top_features_by_class(matrix, y, features, min_tfidf=0.1, top_n=25):
    ''' Return a list of dfs, where each df holds top_n features and their mean tfidf value
        calculated across documents with the same class label. '''
    dfs = []
    labels = np.unique(y)
    for label in labels:
        ids = np.where(y == label)
        feats_df = top_mean_features(matrix, features, ids, min_tfidf=min_tfidf, top_n=top_n)
        feats_df.label = label
        dfs.append(feats_df)
    return dfs


def top_mean_features_v2(matrix, features, grp_ids=None, anti_ids=None, min_tfidf=0.1, top_n=25):
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
    ''' Return a list of dfs, where each df holds top_n features and their mean tfidf value
        calculated across documents with the same class label. '''
    dfs = []
    labels = np.unique(y)
    for label in labels:
        ids = np.where(y == label)
        anti_ids = np.where(y != label)
        feats_df = top_mean_features_v2(
            matrix, features, grp_ids=ids, anti_ids=anti_ids, min_tfidf=min_tfidf, top_n=top_n
        )
        feats_df.label = label
        dfs.append(feats_df)
    return dfs


def plot_tfidf_classfeats_h(dfs):
    ''' Plot the data frames returned by the function plot_tfidf_classfeats(). '''
    fig = plt.figure(figsize=(12, 9), facecolor="w")
    x = np.arange(len(dfs[0]))
    for i, df in enumerate(dfs):
        ax = fig.add_subplot(1, len(dfs), i+1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_frame_on(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_xlabel("Mean Tf-Idf Score", labelpad=16, fontsize=14)
        ax.set_title(str(df.label), fontsize=16)
        ax.ticklabel_format(axis='x', style='sci', scilimits=(-2, 2))
        ax.barh(x, df.tfidf, align='center', color='#3F5D7D')
        ax.set_yticks(x)
        ax.set_ylim([-1, x[-1]+1])
        yticks = ax.set_yticklabels(df.feature)
        plt.subplots_adjust(bottom=0.09, right=0.97, left=0.15, top=0.95, wspace=0.52)
    plt.show()


if __name__ == "__main__":
    start_time = time.time()

    data = open_data()

    vectorizer, matrix = vectorize_articles(data[TEXT_COL])
    X = add_metadata_to_tfidf_mat(matrix, data, vectorizer)

    X.to_csv(VECTORIZED_PATH, encoding='utf-8')

    seconds = time.time() - start_time
    minutes = seconds / 60
    print("Vectorizer took", minutes, "minutes to run")

    # print top used words:
    features = vectorizer.get_feature_names()
    print(top_mean_features(matrix, features, min_tfidf=0.0, top_n=35))

    # print top features of each class:
    y = data[LABEL_COL]
    dfs = top_features_by_class_v2(matrix, y, features, min_tfidf=0.0, top_n=10)
    plot_tfidf_classfeats_h(dfs)
