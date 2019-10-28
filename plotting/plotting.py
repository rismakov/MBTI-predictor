from __future__ import division, print_function

import logging 
import numpy as np
import pandas as pd

from collections import OrderedDict

from data_transformation.vectorize_data import top_features_by_class_v2
from plotting_constants import (
    FUNCTION_PAIRS, 
    GLOBAL_PERCENTAGES,
    LETTERS,
)
from plotting_utils import (
    add_title, label_fig_xaxis, plot_bar_graph, plot_table, save_fig
)
from utils.color_constants import (
    COLOR_MAPPINGS,
    FACECOLOR,
    LETTER_COLOR_MAPPINGS, 
    LETTER_PLOT_COLORS, 
    PLOT_COLORS,
    ZODIAC_PLOT_COLORS,
)
from utils.constants import (
    FEATURIZED_PATH, 
    FUNCTION_INDS,
    FUNCTION_PLOTS_PATH, 
    LABEL_COL, 
    MBTI_TYPES, 
    PLOTS_PATH, 
    TEXT_COL, 
    TFIDF_MAX_FEATURES,
    VECTORIZED_PATH
)
from utils.utils import (
    convert_df_to_sparse_mat, 
    explode_df, 
    get_label_percentages, 
    open_data, 
    open_textfile,
)

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

logging.getLogger().setLevel(logging.INFO)

def run_through_all_letter_types(f, *args):
    for letters in FUNCTION_PAIRS:
        f(*args)

def subplot_distribution_info(
    subplot_ind, dist_data, y_label, plot_colors='black'
):
    """Plot distribution of data.

    Parameters
    ----------

    """
    plt.subplot(3, 1, subplot_ind)
    plot_bar_graph(
        x_values=list(range(len(dist_data))), 
        y_values=dist_data.values(), 
        x_labels=dist_data.keys(), 
        color=plot_colors
    )

    plt.ylabel(y_label, fontsize=10)

def get_distribution_diff(data_label_percentages, global_percentages):
    """Return the distribution difference between data set and global values.

    `data_label_percentages` can be the percentages for the full label (i.e. 
    `entp`, `esfj`, etc) or for the individual letters (`E`, `J`, `P`.)

    NOTE: `global_percentages` and `data_label_percentages` should be the same 
    length.

    Parameters
    ----------
    data_label_percentages : OrderedDict
        The distribution of the data set labels.
    global_percentages : OrderedDict
        The distribution of the global percentages.
    
    Returns
    -------
    OrderedDict
        The difference between the values. 
    """
    return OrderedDict([
        (
            mbti_type, round(
                data_label_percentages[mbti_type] 
                - global_percentages[mbti_type], 2
            )
        ) for mbti_type in data_label_percentages.keys()
    ])
    
def get_letter_percents_from_type_percents(counts):
    """Get the distribution of individual MBTI-letters from full MBTI type data.

    Parameters
    ----------
    counts : dict
        The distribution of the MBTI types. Length of `counts` should be 16.
    
    Returns
    -------
    dict
        Returns dict with keys as all MBTI individual letter labels and values 
        as the percentages. Length of dict returned should be 8.   
    """

    def combine_letter_counts(counts, letter):
        return sum(
            count for mbti_type, count in counts.items() if letter in mbti_type
        )

    return OrderedDict([
        (letter, combine_letter_counts(counts, letter)) for letter in LETTERS
    ])

def plot_personality_type_distributions(data, facecolor=FACECOLOR):
    """Plot label distributions.

    Plots two figures with 3 subplots each (data set, global, and difference).
    """
    # get values for full mbti types
    data_label_percentages = OrderedDict(
        # sorts index in same order as `MBTI_TYPES`
        get_label_percentages(data, LABEL_COL)[MBTI_TYPES]
    )
    type_distributions = OrderedDict([
        ('data distribution', data_label_percentages), 
        ('global distribution', GLOBAL_PERCENTAGES), 
        ('distribution difference', get_distribution_diff(
            data_label_percentages, GLOBAL_PERCENTAGES)
        )    
    ])
    logging.info('Calculated distributions for full MBTI types')

    # get values for individual mbti type-letters
    data_letter_percentages = get_letter_percents_from_type_percents(
        data_label_percentages
    )
    global_letter_percentages = get_letter_percents_from_type_percents(
        GLOBAL_PERCENTAGES
    )
    letter_distributions = OrderedDict([
        ('data distribution', data_letter_percentages),
        ('global distribution', global_letter_percentages),
        ('distribution difference', get_distribution_diff(
            data_letter_percentages, global_letter_percentages)
        )
    ])
    logging.info('Calculated distributions for individual MBTI type-letters')

    for dist_info, colors, filename in zip(
        (type_distributions, letter_distributions),
        (PLOT_COLORS, LETTER_PLOT_COLORS),
        ('type_distributions', 'type_distributions_by_letter'),
    ):
        plt.figure(figsize=(5, 10))

        subplot_ind = 1
        for dist_description, dist_data in dist_info.items():
            subplot_distribution_info(
                subplot_ind, 
                dist_data, 
                y_label=dist_description, 
                plot_colors=colors
            )

            logging.info(
                'Plotted {} in subplot {}'.format(dist_description, subplot_ind)
            )
            subplot_ind += 1
        output_path = 'graphs/{}'.format(filename)
        save_fig(output_path, facecolor=facecolor)
        logging.info('Saved plot to {}'.format(output_path))


def get_marker_color(mbti_type):
    '''If looking at full MBTI type, returns color depending on value of COLOR_MAPPINGS when keying by the first two
    letters. Otherwise returns 'black' if not looking at the full MBTI type.
    '''
    if len(mbti_type) == 4:
        return COLOR_MAPPINGS[mbti_type[:2]]
    
    if len(mbti_type) == 1:
        return LETTER_COLOR_MAPPINGS[mbti_type]

    return 'black'


def errorbar_graph_of_mean_feature_values(means, errs, xaxis_names, feature):
    for i, mean, err, name in zip(range(len(means)), means, errs, xaxis_names):
        group_color = get_marker_color(name)
        plt.errorbar(i, mean, yerr=err, fmt='o', color=group_color, alpha=0.8)

    label_fig_xaxis(xaxis_names)


def is_statistically_significant(lower_bounds, upper_bounds, letter_1, letter_2):
    '''Check if the difference is statistically significant.
    '''
    return (
        (lower_bounds[letter_1] > upper_bounds[letter_2]) 
        or (lower_bounds[letter_2] > upper_bounds[letter_1])
    )

def extract_lower_and_upper_bounds(data, group_by_col, feature):
    """Get means, errors, and error bar values for error bar plot.

    Parameters
    ----------
    data : pandas.DataFrame
        Data to observe.
    group_by_col : str
        The column to group by (will be the column with the values for the 
        xtick-labels -- i.e. `mbti_type` or `extroversion-introversion` or for 
        zodiac analysis one of the zodiac features ex: `leo`).
    feature : str
        The feature we are looking at (i.e. the title of the plot).
    """
    means = data.groupby(group_by_col).mean()
    sems = data.groupby(group_by_col).sem()

    feature_means = means[feature]
    feature_sems = sems[feature]

    lower_bounds = feature_means - feature_sems
    upper_bounds = feature_means + feature_sems

    return feature_means, feature_sems, lower_bounds, upper_bounds


def group_and_plot_by_type(
    data, group_by_col, feature, i=1, n=1, m=1, with_subplots=False
):
    feature_means, feature_sems, lower_bounds, upper_bounds = (
        extract_lower_and_upper_bounds(data, group_by_col, feature)
    )

    if with_subplots:
        unique_values = np.unique(data[group_by_col].values)
        assert len(unique_values) == 2
        
        dimension_value_1, dimension_value_2 = unique_values

        plt.subplot(n, m, i + 1)

    errorbar_graph_of_mean_feature_values(
        feature_means, 
        feature_sems, 
        feature_sems.index, 
        feature, 
    )


def plot_all_graphs(data, features, cols_to_group_by):
    '''Plot errorbar graphs for all types and errorbar graphs for all types separated by letter-type in 4 subplot
    figures. Only plots subplot if results are statistically significant.
    '''
    for feature in features:
        # plot figure of feature means with four subplots for each function 
        # dimension ('E-I', 'N-S', 'F-T', and 'J-P').
        fig = plt.figure()
        for i, type_dimension in enumerate(cols_to_group_by):
            group_and_plot_by_type(
                data, type_dimension, feature, i, 2, 2, with_subplots=True
            )
            plt.yticks(fontsize=8)

        fig.suptitle(feature, fontsize=13)

        filename_to_save = '{}/{}'.format(
            FUNCTION_PLOTS_PATH, feature.replace('.', '')
        )
        save_fig(filename_to_save, facecolor=FACECOLOR)

        # plot figure of feature means for full MBTI types
        fig = plt.figure()
        group_and_plot_by_type(data, LABEL_COL, feature, 1, 1, 1)
        plt.yticks(fontsize=8)

        fig.suptitle(feature, fontsize=13)
        filename_to_save = '{}/{}'.format(PLOTS_PATH, feature.replace('.', ''))
        save_fig(filename_to_save, facecolor=FACECOLOR)

def plot_fig_with_zodiac_signs(data, zodiacs, output_filename):
    fig = plt.figure()
    for feature in zodiacs:
        group_and_plot_by_type(
            data, zodiac, mbti_type, 1, 1, 1
        )
    
    plt.yticks(fontsize=8)
    plt.legend(zodiacs)

    fig.suptitle(feature, fontsize=13)
    save_fig(output_filename, facecolor=FACECOLOR)
    plt.close()

def plot_zodiac_info(data, cols_to_group_by):
    fire_signs = ['aries', 'leo', 'sagittarius']
    water_signs = ['pisces', 'cancer', 'scorpio']
    earth_signs = ['taurus', 'virgo', 'capricorn']
    air_signs = ['aquarius', 'gemini', 'libra']

    zodiacs = fire_signs + water_signs + earth_signs + air_signs
    zodiacs = [x for x in zodiacs if x in data.columns]    

    zodiac_data = data[zodiacs + [LABEL_COL]]

    for mbti_type in MBTI_TYPES:
        logging.info('Checking zodiac usage for MBTI type {}'.format(mbti_type))

        subset_data = zodiac_data.loc[
            zodiac_data[LABEL_COL] == mbti_type, :
        ].drop(LABEL_COL, axis=1)
        logging.info('Subset data for mbti type {} has {} rows'.format(
            mbti_type, len(subset_data))
        )
        
        means = subset_data.apply(lambda x: x.mean(), axis=1)
        sems = subset_data.apply(lambda x: x.sem(), axis=1)
        
        fig = plt.figure()
        plt.errorbar(range(len(means)), means, yerr=sems, fmt='o', alpha=0.8)

        label_fig_xaxis(zodiac_data.columns)
        fig.suptitle(mbti_type, fontsize=13)
        filename_to_save = 'graphs/zodiac_{}'.format(mbti_type)
        save_fig(filename_to_save, facecolor=FACECOLOR)


def compare_types(data, group_by_col, all_types_to_compare, features):
    for col_to_group_by, letter_types in zip(cols_to_group_by, all_types_to_compare):

        higher_key = '{}_higher'

        letter_type_results = {}
        for letter_type in letter_types:
            letter_type_results[higher_key.format(letter_type)] = []

        for feature in features:
            _, _, lower_bounds, upper_bounds = extract_lower_and_upper_bounds(
                data, group_by_col, feature
            )

            letter_1, letter_2 = (letter_types[0], letter_types[1])
            if is_statistically_significant(
                lower_bounds, upper_bounds, letter_1, letter_2
            ):
                max_ind = lower_bounds[lower_bounds == lower_bounds.max()].index
                letter_type_results[
                    higher_key.format(max_ind[0])
                ].append(feature)

        for letter_type in letter_types:
            print('The following features are higher in {} type'
                  .format(FUNCTION_MAPPINGS.get(letter_type, letter_type)))

            for feature in letter_type_results[higher_key.format(letter_type)]:
                print(feature)
            print()


def plot_tfidf_classfeats_h(dfs):
    ''' Plots the DataFrames returned by the function `plot_tfidf_classfeats`.

    :param type dfs: list of Pandas DataFrames.
    '''
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


def get_cell_colors(n, m, color):
    '''Returns list of lists of size (n,m) filled with color specified. Created to be used for plotting table cells.

    :param type n: int.
    :param type m: int.
    :param type color: string specifying color name.
    '''
    return [[color] * n for i in range(m)]


def plot_tfidf_subplot(dfs, start_ind, stop_ind):
    '''Plot subplot of top words of subset of the MBTI types.
    
    Subset determined by start and stop indices specified.

    :param type dfs: list of Pandas DataFrames.
    :param type start_ind: int.
    :parm type stop_ind: int.
    '''
    dfs = dfs[start_ind:stop_ind]
    col_labels = MBTI_TYPES[start_ind:stop_ind]
    col_colors = PLOT_COLORS[start_ind:stop_ind]

    num_of_top_words = len(dfs[0])

    cell_text = [
        [df.feature[ind] for df in dfs] for ind in range(num_of_top_words)
    ]

    num_of_col = len(col_labels)
    num_of_row = len(cell_text)
    cell_colors = get_cell_colors(num_of_col, num_of_row, 'whitesmoke')
    plot_table(cell_text, col_labels=col_labels, col_colors=col_colors)


def plot_tfidf_top_words_table(dfs, split_inds=None, facecolor=FACECOLOR):
    '''Plots and saves top words for each MBTI type. Divides plots into multiple subplots, depending on how split_inds
    (the indicies to split on) are defined.

    :param dfs type: list of Pandas Dataframes with 'feature' and 'tfidf' columns.
    :param split_inds type: list of ints: the indices on which to split the data for plotting.
    '''
    if not split_inds:
        split_inds = [0, len(dfs) + 1]

    plt.figure(figsize=(10, 7))
    num_of_subplots = len(split_inds) - 1
    for i, start_ind in enumerate(split_inds[:-1]):
        stop_ind = split_inds[i+1]

        plt.subplot(num_of_subplots, 1, i+1)
        plot_tfidf_subplot(dfs, start_ind, stop_ind)
    save_fig('graphs/top_words_for_each_type_{}'.format(
        TFIDF_MAX_FEATURES), facecolor=facecolor
    )


def add_relevant_cols_to_data(data):
    for function, (start_ind, stop_ind) in FUNCTION_INDS.items():
        data[function] = [
            mbti_type[start_ind:stop_ind] for mbti_type in data[LABEL_COL]
        ]

    return data


def get_words_to_plot(dfs, featurized_data):
    """Get all top TFIDF words for all types.
    """
    all_top_words = []
    for df in dfs:
        all_top_words += list(df.feature.values)

    features = (
        list(featurized_data.columns.remove(LABEL_COL)) 
        + list(set(all_top_words)) 
        + ['mother'] 
    )
    # features.remove(LABEL_COL)

    return features


if __name__ == "__main__":
    featurized_data = pd.read_csv(
        FEATURIZED_PATH, encoding='utf-8').drop(['Unnamed: 0'], axis=1
    )
    logging.info(
        'Loaded featurized data of size {}'.format(len(featurized_data))
    )
    vectorized_data = pd.read_csv(
        VECTORIZED_PATH, encoding='utf-8').drop(['Unnamed: 0'], axis=1
    )
    logging.info(
        'Loaded vectorized data of size {}'.format(len(vectorized_data))
    )

    data = pd.concat([featurized_data, vectorized_data], axis=1)
    data = add_relevant_cols_to_data(data)

    # plot distributions of data:
    # plot_personality_type_distributions(data)

    vectorized_matrix = convert_df_to_sparse_mat(vectorized_data)
    
    features = open_textfile()
    logging.info('Loaded list of {} features'.format(len(features)))
    
    y = data[LABEL_COL]
    top_word_features_dfs = top_features_by_class_v2(
        vectorized_matrix, y, features, min_tfidf=0.0, top_n=15
    )

    # plot top-TFIDF-words table
    # logging.info('Plotting top TFIDF words for each MBTI type.')
    # plot_tfidf_top_words_table(top_word_features_dfs, split_inds=[0, 8, 16])
    
    cols_to_group_by = [
        'Extraversion-Introversion', 
        'Intuition-Sensing',
        'Feeling-Thinking',
        'Judging-Perceiving',
    ]
    
    plot_zodiac_info(data, cols_to_group_by)

    # only plot the strong signals
    '''
    features_to_plot = get_words_to_plot(
        top_word_features_dfs, featurized_data
    )
    features_to_plot = [x for x in features_to_plot if x in data.columns]
    logging.info('Plotting {} different features'.format(len(features_to_plot)))
    plot_all_graphs(data, features_to_plot, cols_to_group_by)
    '''

    # run below for comparisons:
    # all_types_to_compare = [['E', 'I'], ['N', 'S'], ['F', 'T'], ['J', 'P']]
    # compare_types(data, cols_to_group_by, all_types_to_compare, features)

    # run below to compare any two types to each other
    # cols_to_group_by = ['type']
    # all_types_to_compare = [['ENTP', 'INFP']]
    # data_minimized = data.loc[data[cols_to_group_by[0]].isin(all_types_to_compare[0])]
    # compare_types(data_minimized, cols_to_group_by, all_types_to_compare, features)
