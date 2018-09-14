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

xaxis_mappings = {
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


def group_and_plot_by_type(data, group_by_col, feature):
    means = data.groupby(group_by_col).mean()
    sems = data.groupby(group_by_col).sem()

    plt.style.use('fivethirtyeight')
    feature_means = means[feature]
    feature_sems = sems[feature]

    if len(group_by_col) == 2:
        lower_bounds = feature_means - feature_sems
        upper_bounds = feature_means + feature_sems
        
        letter_1 = group_by_col[0]
        letter_2 = group_by_col[-1]
        # only plot if difference is statistically significant
        if ((lower_bounds[letter_1] > upper_bounds[letter_2]) or
            (lower_bounds[letter_2] > upper_bounds[letter_1])):

            plt.subplot(2, 2, i+1)
            errorbar_graph_of_mean_feature_values(feature_means, feature_sems, feature_sems.index, feature)
    else:
        errorbar_graph_of_mean_feature_values(feature_means, feature_sems, feature_sems.index, feature)        

if __name__ == "__main__":
    path = '../MBTI_project/featurized_mbti'
    data = pd.read_csv(path, encoding='utf-8')

    features = list(data.columns)   
    for field_to_remove in ['Unnamed: 0', 'type', 'posts']:
        features.remove(field_to_remove)

    print(features)

    data['EI'] = [mbti_type[0] for mbti_type in data['type']]
    data['NS'] = [mbti_type[1] for mbti_type in data['type']]
    data['FT'] = [mbti_type[2] for mbti_type in data['type']]
    data['JP'] = [mbti_type[3] for mbti_type in data['type']]
    data['1_2'] = [mbti_type[0:2] for mbti_type in data['type']]
    data['2_3'] = [mbti_type[1:3] for mbti_type in data['type']]
    data['1_3_4'] = [mbti_type[0:1] + mbti_type[2:4] for mbti_type in data['type']]
    
    letter_types = ['EI', 'NS', 'FT', 'JP']

    for feature in features:
        plt.figure()
        plt.title(feature)
        for i, letter_type in enumerate(letter_types):
            group_and_plot_by_type(data, letter_type, feature)

        filename_to_save = '../MBTI_project/plots/' + feature
        plt.savefig(filename_to_save, facecolor='whitesmoke')
        plt.close()

        group_and_plot_by_type(data, 'type', feature)
        filename_to_save = '../MBTI_project/plots/' + feature + '_all'
        plt.savefig(filename_to_save, facecolor='whitesmoke')
        plt.close()


