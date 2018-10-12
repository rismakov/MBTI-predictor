from __future__ import division, print_function

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

color_mappings = {
    'EN': 'dodgerblue',
    'ES': 'slategray',
    'IN': 'lightseagreen',
    'IS': 'salmon',
    'E': 'orangered',
    'I': 'forestgreen',
    'N': 'c',
    'S': 'lightpink',
    'T': 'mediumseagreen',
    'F': 'mediumpurple',
    'J': 'gray',
    'P': 'chocolate'
}    

type_mappings = {
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


def label_fig_xaxis_names(names, width=0):
    x_range = np.arange(len(names))
    plt.xticks(x_range + width, names, rotation='vertical')
    plt.xlim([x_range.min()-0.5, x_range.max()+0.5 + width])

    
def errorbar_graph_of_mean_feature_values(means, errs, xaxis_names, feature):
    for i, mean, err, name in zip(range(len(means)), means, errs, xaxis_names):
        if len(name) > 1:
            color = color_mappings.get(name[0:2], 'skyblue')
        elif len(name) == 1:
            color = color_mappings[name]

        plt.errorbar(i, mean, yerr=err, fmt='o', color=color, alpha=0.8)

    # names = [xaxis_mappings.get(name, name) for name in xaxis_names]
    label_fig_xaxis_names(xaxis_names)


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

    plt.style.use('fivethirtyeight')
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
        plt.title(feature)
        for i, letter_type in enumerate(letter_types):
            group_and_plot_by_type(data, letter_type, feature, i, 2, 2)

        filename_to_save = '../MBTI_project/plots/' + feature.replace('.', '')
        plt.savefig(filename_to_save, facecolor='whitesmoke')
        plt.close()

        group_and_plot_by_type(data, 'type', feature, 1, 1, 1)
        filename_to_save = '../MBTI_project/plots/' + feature.replace('.', '') + '_all'
        plt.savefig(filename_to_save, facecolor='whitesmoke')
        plt.close()    


def print_info(data, letter_types, features):
    for i, letter_type in enumerate(letter_types):
        letter_type_results = {}
        
        higher_key = '{}_higher'
        for i in xrange(2):
            letter_type_results[higher_key.format(letter_type[i])] = []
        
        for feature in features:
            _, _, lower_bounds, upper_bounds = extract_lower_and_upper_bounds(data, letter_type, feature)

            letter_1, letter_2 = (letter_type[0], letter_type[1])
            if is_statistically_significant(lower_bounds, upper_bounds, letter_1, letter_2):
                max_ind = lower_bounds[lower_bounds == lower_bounds.max()].index
                letter_type_results[higher_key.format(max_ind[0])].append(feature)

        for i in xrange(2):
            letter = letter_type[i]
            print('The following features are higher in {} type'.format(type_mappings[letter]))
            for feature in letter_type_results[higher_key.format(letter)]:
                print(feature)
            print()


if __name__ == "__main__":
    path = '../MBTI_project/featurized_mbti'
    data = pd.read_csv(path, encoding='utf-8')

    features = list(data.columns)   
    for field_to_remove in ['Unnamed: 0', 'type', 'posts']:
        features.remove(field_to_remove)

    print('Features:')
    print(features)

    data['EI'] = [mbti_type[0] for mbti_type in data['type']]
    data['NS'] = [mbti_type[1] for mbti_type in data['type']]
    data['FT'] = [mbti_type[2] for mbti_type in data['type']]
    data['JP'] = [mbti_type[3] for mbti_type in data['type']]
    data['1_2'] = [mbti_type[0:2] for mbti_type in data['type']]
    data['2_3'] = [mbti_type[1:3] for mbti_type in data['type']]
    data['1_3_4'] = [mbti_type[0:1] + mbti_type[2:4] for mbti_type in data['type']]
    
    letter_types = ['EI', 'NS', 'FT', 'JP']

    plot_all_graphs(data, features, letter_types)

    print_info(data, letter_types, features)
