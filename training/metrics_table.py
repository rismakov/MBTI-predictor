import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from constants import COLOR_INCREASE, LETTER_TYPES, TABLE_COLORS
from plotting.plotting_utils import plot_table, save_fig

def print_results_in_table(metrics, clfs, clf_names, filename):
    fig, ax = plt.subplots()

    scoring_types = []
    for letter_type in [''] + LETTER_TYPES:
        for scoring_type in ['accuracy', 'precision', 'recall', 'f1']:
            scoring_types.append(
                '_'.join([x for x in ['test', letter_type, scoring_type] if x])
            )

    # metrics [clf name] [scoring type]
    cell_text = [
        ['{:.2f}'.format(
            metrics[clf_name][scoring_type] * 100.0
        ) for clf_name in clf_names] for scoring_type in scoring_types
    ]

    cell_colors = [[color] * len(clfs) for color in TABLE_COLORS]

    cell_text_ints = [[float(x) for x in lst] for lst in cell_text]
    max_clf_inds = [lst.index(max(lst)) for lst in cell_text_ints]
    for metric_ind, clf_ind in enumerate(max_clf_inds):
        current_color = cell_colors[metric_ind][clf_ind]
        cell_colors[metric_ind][clf_ind] = COLOR_INCREASE[current_color]

    plot_table(cell_text, scoring_types, clf_names, cell_colors=cell_colors)

    save_fig(filename)
