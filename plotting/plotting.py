from __future__ import division, print_function

import numpy as np
import pandas as pd

from collections import OrderedDict

from data_transformation.vectorize_data import top_features_by_class_v2
from plotting_constants import COLOR_MAPPINGS, GLOBAL_PERCENTAGES, PLOT_COLORS
from plotting_utils import add_title, label_fig_xaxis, plot_bar_graph, plot_table, save_fig
from utils.constants import (
    FEATURIZED_PATH, FUNCTION_PLOTS_PATH, LABEL_COL, MBTI_TYPES_UPPER, PLOTS_PATH, VECTORIZED_PATH
)
from utils.utils import convert_df_to_sparse_mat, get_distribution_of_ylabel_classes, open_textfile

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


FUNCTION_MAPPINGS = {
    'EN': 'Extraversion-Intuition',
    'ES': 'Extraversion-Sensing',
    'IN': 'Introversion-Intuition',
    'IS': 'Introversion-Sensing',
    'E': 'Extraversion',
    'I': 'Introversion',
    'N': 'Intuition',
    'S': 'Sensing',
    'T': 'Thinking',
    'F': 'Feeling',
    'J': 'Judging',
    'P': 'Perceiving'
}

FUNCTION_INDS = {
    'EI': [0, 1],
    'NS': [1, 2],
    'FT': [2, 3],
    'JP': [3, 4],
    '1_2': [0, 2],
    '2_3': [2, 3]
}


plt.style.use('fivethirtyeight')


def plot_type_percentages(data):
    type_percentages = get_distribution_of_ylabel_classes(data, LABEL_COL)

    distribution_diffs = {
        mbti_type: type_percentages[mbti_type] - GLOBAL_PERCENTAGES[mbti_type] for mbti_type in MBTI_TYPES_UPPER
    }

    info = OrderedDict({
        'data distribution': type_percentages,
        'global distribution': GLOBAL_PERCENTAGES,
        'distribution difference':  distribution_diffs
    })

    xvalues = list(range(len(MBTI_TYPES_UPPER)))

    plt.figure(figsize=(5, 10))
    for i, distribution_data in enumerate(info.items()):
        name, percent_data = distribution_data

        yvalues = [percent_data[mbti_type] for mbti_type in MBTI_TYPES_UPPER]

        plt.subplot(3, 1, i+1)
        plot_bar_graph(xvalues, yvalues, MBTI_TYPES_UPPER, color=PLOT_COLORS)
        plt.ylabel(name, fontsize=10)
    save_fig('type_distributions')


def get_marker_color(mbti_type):
    '''If looking at full MBTI type, returns color depending on value of COLOR_MAPPINGS when keying by the first two
    letters. Otherwise returns 'black' if not looking at the full MBTI type.
    '''
    if len(mbti_type) == 4:
        return COLOR_MAPPINGS[mbti_type[:2]]

    return 'black'


def errorbar_graph_of_mean_feature_values(means, errs, xaxis_names, feature):
    for i, mean, err, name in zip(range(len(means)), means, errs, xaxis_names):
        group_color = get_marker_color(name)
        plt.errorbar(i, mean, yerr=err, fmt='o', color=group_color, alpha=0.8)

    add_title(feature)

    label_fig_xaxis(xaxis_names)


def is_statistically_significant(lower_bounds, upper_bounds, letter_1, letter_2):
    return (
        (lower_bounds[letter_1] > upper_bounds[letter_2]) or
        (lower_bounds[letter_2] > upper_bounds[letter_1])
    )


def extract_lower_and_upper_bounds(data, group_by_col, feature):
    means = data.groupby(group_by_col).mean()
    sems = data.groupby(group_by_col).sem()

    feature_means = means[feature]
    feature_sems = sems[feature]

    lower_bounds = feature_means - feature_sems
    upper_bounds = feature_means + feature_sems

    return feature_means, feature_sems, lower_bounds, upper_bounds


def group_and_plot_by_type(data, group_by_col, feature, i, n, m):
    feature_means, feature_sems, lower_bounds, upper_bounds = extract_lower_and_upper_bounds(
        data, group_by_col, feature)

    if len(group_by_col) == 2:
        letter_1 = group_by_col[0]
        letter_2 = group_by_col[-1]
        # only plot if difference is statistically significant
        if is_statistically_significant(lower_bounds, upper_bounds, letter_1, letter_2):
            plt.subplot(n, m, i+1)
            errorbar_graph_of_mean_feature_values(feature_means, feature_sems, feature_sems.index, feature)
    else:
        errorbar_graph_of_mean_feature_values(feature_means, feature_sems, feature_sems.index, feature)


def plot_all_graphs(data, features, letter_types):
    '''Plots errorbar graphs for all types and plots errorbar graphs for all types separated by letter-type in 4 subplot
    figures. Only plots subplot if results are statistically significant.
    '''
    for feature in features:
        plt.figure()
        add_title(feature)
        for i, letter_type in enumerate(letter_types):
            group_and_plot_by_type(data, letter_type, feature, i, 2, 2)

        filename_to_save = '{}/{}'.format(FUNCTION_PLOTS_PATH, feature.replace('.', ''))
        save_fig(filename_to_save)
        plt.close()

        group_and_plot_by_type(data, LABEL_COL, feature, 1, 1, 1)
        filename_to_save = '{}/{}'.format(PLOTS_PATH, feature.replace('.', ''))
        save_fig(filename_to_save)
        plt.close()


def compare_types(data, cols_to_group_by, all_types_to_compare, features):
    for col_to_group_by, letter_types in zip(cols_to_group_by, all_types_to_compare):

        higher_key = '{}_higher'

        letter_type_results = {}
        for letter_type in letter_types:
            letter_type_results[higher_key.format(letter_type)] = []

        for feature in features:
            _, _, lower_bounds, upper_bounds = extract_lower_and_upper_bounds(data, col_to_group_by, feature)

            letter_1, letter_2 = (letter_types[0], letter_types[1])
            if is_statistically_significant(lower_bounds, upper_bounds, letter_1, letter_2):
                max_ind = lower_bounds[lower_bounds == lower_bounds.max()].index
                letter_type_results[higher_key.format(max_ind[0])].append(feature)

        for letter_type in letter_types:
            print('The following features are higher in {} type'
                  .format(FUNCTION_MAPPINGS.get(letter_type, letter_type)))

            for feature in letter_type_results[higher_key.format(letter_type)]:
                print(feature)
            print()


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


def plot_tfidf_top_words_table(dfs):
    size_of_dfs = len(dfs[0])

    cell_text = [[df.feature[ind] for df in dfs] for ind in range(size_of_dfs)]

    print(cell_text)

    plot_table(cell_text, col_labels=MBTI_TYPES_UPPER[:8], col_colors=PLOT_COLORS)

    plt.show()


def add_relevant_cols_to_data(data):
    for function, function_inds in FUNCTION_INDS.items():
        start_ind, stop_ind = function_inds
        data[function] = [mbti_type[start_ind:stop_ind] for mbti_type in data[LABEL_COL]]

    data['1_3_4'] = [mbti_type[0:1] + mbti_type[2:4] for mbti_type in data[LABEL_COL]]

    return data


if __name__ == "__main__":
    featurized_data = pd.read_csv(FEATURIZED_PATH, encoding='utf-8').drop(['Unnamed: 0'], axis=1)
    vectorized_data = pd.read_csv(VECTORIZED_PATH, encoding='utf-8').drop(['Unnamed: 0'], axis=1)

    data = pd.concat([featurized_data, vectorized_data], axis=1)

    # plot_type_percentages(featurized_data)
    data = add_relevant_cols_to_data(data)

    vectorized_matrix = convert_df_to_sparse_mat(vectorized_data)
    features = open_textfile()

    print(features)

    y = data[LABEL_COL]

    # print top used words:
    dfs = top_features_by_class_v2(vectorized_matrix, y, features, min_tfidf=0.0, top_n=15)
    plot_tfidf_top_words_table(dfs[:8])

    '''
    features = list(featurized_data.columns) + TOP_WORDS
    features.remove(LABEL_COL)


    cols_to_group_by = ['EI', 'NS', 'FT', 'JP']
    all_types_to_compare = [['E', 'I'], ['N', 'S'], ['F', 'T'], ['J', 'P']]

    # plot_all_graphs(data, features, cols_to_group_by)

    compare_types(data, cols_to_group_by, all_types_to_compare, features)

    # run below to compare any NTs and NFs
    cols_to_group_by = ['2_3']
    all_types_to_compare = [['NT', 'NF']]
    data_minimized = data.loc[data[cols_to_group_by[0]].isin(all_types_to_compare[0])]
    compare_types(data_minimized, cols_to_group_by, all_types_to_compare, features)

    # run below to compare any two types to each other
    cols_to_group_by = ['type']
    all_types_to_compare = [['ENTP', 'INFP']]
    data_minimized = data.loc[data[cols_to_group_by[0]].isin(all_types_to_compare[0])]
    compare_types(data_minimized, cols_to_group_by, all_types_to_compare, features)
    '''
