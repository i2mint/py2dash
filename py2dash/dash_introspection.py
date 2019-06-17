import importlib

import matplotlib.pylab as plt

import dash_core_components as dcore
import dash_html_components as hcore

from py2dash.misc import module_classes_signatures_df, non_null_counts


def heatmap(X, y=None, col_labels=None, figsize=None, cmap=None, return_gcf=False, ax=None,
            xlabel_top=True, ylabel_left=True, xlabel_bottom=True, ylabel_right=True, **kwargs):
    import pandas as pd
    import numpy as np
    n_items, n_cols = X.shape
    if col_labels is not None:
        if col_labels is not False:
            assert len(col_labels) == n_cols, \
                "col_labels length should be the same as the number of columns in the matrix"
    elif isinstance(X, pd.DataFrame):
        col_labels = list(X.columns)

    if figsize is None:
        x_size, y_size = X.shape
        if x_size >= y_size:
            figsize = (6, min(18, 6 * x_size / y_size))
        else:
            figsize = (min(18, 6 * y_size / x_size), 6)

    if cmap is None:
        if X.min(axis=0).min(axis=0) < 0:
            cmap = 'RdBu_r'
        else:
            cmap = 'hot_r'

    kwargs['cmap'] = cmap
    kwargs = dict(kwargs, interpolation='nearest', aspect='auto')

    if figsize is not False:
        plt.figure(figsize=figsize)

    if ax is None:
        plt.imshow(X, **kwargs)
    else:
        ax.imshow(X, **kwargs)
    plt.grid(None)

    if y is not None:
        y = np.array(y)
        assert all(sorted(y) == y), "This will only work if your row_labels are sorted"

        unik_ys, unik_ys_idx = np.unique(y, return_index=True)
        for u, i in zip(unik_ys, unik_ys_idx):
            plt.hlines(i - 0.5, 0 - 0.5, n_cols - 0.5, colors='b', linestyles='dotted', alpha=0.5)
        plt.hlines(n_items - 0.5, 0 - 0.5, n_cols - 0.5, colors='b', linestyles='dotted', alpha=0.5)
        plt.yticks(unik_ys_idx + np.diff(np.hstack((unik_ys_idx, n_items))) / 2, unik_ys)
    elif isinstance(X, pd.DataFrame):
        y_tick_labels = list(X.index)
        plt.yticks(list(range(len(y_tick_labels))), y_tick_labels);

    if col_labels is not None:
        plt.xticks(list(range(len(col_labels))), col_labels)
    else:
        plt.xticks([])

    plt.gca().xaxis.set_tick_params(labeltop=xlabel_top, labelbottom=xlabel_bottom)
    plt.gca().yaxis.set_tick_params(labelleft=ylabel_left, labelright=ylabel_right)

    if return_gcf:
        return plt.gcf()


def heatmap_of_module_classes_signatures(module='dash_core_components', figsize=(15, 25)):
    if isinstance(module, str):
        module = importlib.import_module(module)
    core_comp_df = module_classes_signatures_df(module)
    heatmap(core_comp_df != '', figsize=figsize);
    plt.xticks(rotation=90)
    plt.grid(False)
    plt.show()


def dcore_heatmap(figsize=(15, 30)):
    heatmap_of_module_classes_signatures(dcore, figsize=figsize)


def hcore_heatmap(figsize=(17, 25)):
    heatmap_of_module_classes_signatures(hcore, figsize=figsize)


def plot_nonnull_counts_of_classes_signatures(module='dash_core_components',
                                              n_top_items=50, figsize=(15, 15), hspace=0.5):
    if isinstance(module, str):
        module = importlib.import_module(module)
    core_comp_df = module_classes_signatures_df(module)
    t, tt = non_null_counts(core_comp_df, null_val='')
    plt.figure(figsize=figsize)
    plt.subplot(2, 1, 1)
    t.iloc[:n_top_items].plot(kind='bar')
    plt.subplot(2, 1, 2)
    tt.iloc[:n_top_items].plot(kind='bar')
    plt.subplots_adjust(hspace=hspace)
    plt.show()


def dcore_plot_nonnull_counts_of_classes_signatures(figsize=(15, 30)):
    heatmap_of_module_classes_signatures(dcore, figsize=figsize)


def hcore_plot_nonnull_counts_of_classes_signatures(figsize=(17, 25)):
    heatmap_of_module_classes_signatures(hcore, figsize=figsize)


if __name__ == '__main__':
    import argh

    argh.dispatch_commands([heatmap_of_module_classes_signatures,
                            plot_nonnull_counts_of_classes_signatures])

