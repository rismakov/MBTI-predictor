import matplotlib.pyplot as plt

from constants import COLORS, COLOR_INCREASE, LETTER_TYPES 


def print_results_in_table(metrics, clfs, clf_names):
    fig, ax = plt.subplots()

    all_ordered_keys = []
    for letter_type in [''] + [letter + '_' for letter in LETTER_TYPES]:
        for scoring_type in ['accuracy', 'precision', 'recall', 'f1']:
            all_ordered_keys.append('test_' + letter_type + scoring_type)

    scoring_types = all_ordered_keys

    # metrics [clf name] [scoring type]
    cell_text = [
        ['{:.2f}'.format(metrics[clf_name][scoring_type] * 100.0) for clf_name in clf_names] 
        for scoring_type in scoring_types
    ]

    cell_colors = [[color] * len(clfs) for color in COLORS]

    cell_text_ints = [[float(x) for x in lst] for lst in cell_text]
    max_clf_inds = [lst.index(max(lst)) for lst in cell_text_ints]
    for metric_ind, clf_ind in enumerate(max_clf_inds):
        current_color = cell_colors[metric_ind][clf_ind]
        cell_colors[metric_ind][clf_ind] = COLOR_INCREASE[current_color]

    # ax.axis('tight')
    ax.axis('off')
    table = ax.table(
        cellText=cell_text, cellColours=cell_colors,
        # cellColours=None,
        # cellLoc='right', colWidths=None,
        rowLabels=scoring_types, rowColours=COLORS, rowLoc='left',
        colLabels=clf_names,  # colColours=None, colLoc='center',
        loc='center'
    )
    
    print('Setting font.')
    table.set_fontsize(14)
    # table.scale(1.5, 3.0)

    # fig.tight_layout()

    print('Saving figure.')
    fig.savefig('table', dpi=100)
    plt.show()
    print('Closing figure.')
    plt.close()
