import pickle

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


def vectorise(meta_data_feature_list, feature_list):

    feature_scalers = {
        feature_name: StandardScaler() for feature_name in feature_list
    }

    data_matrix = np.zeros((len(meta_data_feature_list), len(feature_list)))
    for idx, features in enumerate(meta_data_feature_list):
        data_array = []
        for name, feature in features.items():
            if name not in feature_list:
                continue
            data_array.append(feature)
        data_matrix[idx] = np.asarray(data_array)

    for idx, (scaler_name, scaler) in enumerate(feature_scalers.items()):
        feature_data = data_matrix[:, idx]
        feature_data = feature_data.reshape(-1, 1)
        scaler.fit(feature_data)
        data_matrix[:, idx] = scaler.transform(feature_data).flatten()

    return data_matrix

# THIS CODE IS FROM https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html#sphx-glr-gallery-images-contours-and-fields-image-annotated-heatmap-py
# JUST FOR VISUALIZATION NO STEEL ONLY USE

def heatmap(data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-45, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=("black", "white"), threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # # Loop over the data and create a `Text` for each "pixel".
    # # Change the text's color depending on the data.
    # texts = []
    # for i in range(data.shape[0]):
    #     for j in range(data.shape[1]):
    #         kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
    #         text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
    #         texts.append(text)

    # return texts

if __name__ == '__main__':
    with open('data/data_features.pickle', 'rb') as handle:
        data_features = pickle.load(handle)
    with open('data/features.pickle', 'rb') as handle:
        features = pickle.load(handle)
    with open('data/prediction.pickle', 'rb') as handle:
        predictions = pickle.load(handle)

    data_matrix = vectorise(data_features, features)

    correlation_matrix = np.corrcoef(data_matrix.T)
    correlation_matrix = np.round(correlation_matrix * 100) / 100

    fig, ax = plt.subplots()

    im, cbar = heatmap(correlation_matrix, features, features, ax = ax, cmap = "coolwarm", cbarlabel = "Pearson product-moment")
    annotate_heatmap(im, valfmt = "{x:.1f} t")

    # fig.tight_layout()
    plt.show()
