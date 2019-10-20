import numpy as np

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def label_fig_xaxis(labels, width=0):
    x_range = np.arange(len(labels))
    plt.xticks(x_range + width, labels, rotation='vertical', fontsize=10)
    plt.xlim([x_range.min()-0.5, x_range.max()+0.5 + width])


def plot_bar_graph(x_values, y_values, x_labels, color='black'):
    plt.bar(x_values, y_values, color=color, alpha=0.8)
    label_fig_xaxis(x_labels)


def add_title(title, fontsize=10):
    plt.title(title, fontsize=fontsize)


def save_fig(filename, facecolor='white'):
    plt.savefig(filename, facecolor=facecolor, bbox_inches="tight")
    plt.close()


def plot_table(
    cell_text, 
    row_labels=None, 
    col_labels=None, 
    cell_colors=None, 
    row_colors=None, 
    col_colors=None
):
    table = plt.table(
        cellText=cell_text,
        cellColours=cell_colors, 
        cellLoc='left',
        rowLabels=row_labels, 
        rowColours=row_colors,
        colLabels=col_labels, 
        colColours=col_colors, 
        colLoc='center',
        loc='center'
    )

    table.set_fontsize(10)

    plt.axis('off')  # removes overlayed grid in subplots
