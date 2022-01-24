import pickle

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy.stats.stats import pearsonr

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

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw, location="bottom")
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
    with open('data_features.pickle', 'rb') as handle:
        data_features = pickle.load(handle)
    with open('features.pickle', 'rb') as handle:
        features = pickle.load(handle)
    with open('prediction.pickle', 'rb') as handle:
        predictions = pickle.load(handle)
    with open('re_predict_data.pickle', 'rb') as handle:
        re_predict_data = pickle.load(handle)

    re_predict_distance_score_ocsvm = re_predict_data['path_ocsvm'][-1][2]
    re_predict_distance_score_metadata = re_predict_data['meta_data_model'][-1][2]
    continues_predict_distance_score_ocsvm = list(map(lambda x: 0 if x['distance_to_decision'] is None else x['distance_to_decision'], predictions['path_ocsvm']))
    continues_predict_distance_score_metadata = list(map(lambda x: 0 if x['distance_to_decision'] is None else x['distance_to_decision'], predictions['meta_data_model']))

    model_name = ['Repredict: OCSVM', 'Repredict: Metadata', 'Continues Predict: OCSVM', 'Continues Predict: Metadata']

    data_matrix = vectorise(data_features, features)

    corr_matrix = np.zeros((4, len(features)))
    for idx, feature_name in enumerate(features):
        feature_vector = data_matrix[:, idx]
        asarray = np.asarray(feature_vector)
        corr_matrix[0, idx] = pearsonr(asarray, np.asarray(re_predict_distance_score_ocsvm))[0]
        corr_matrix[1, idx] = pearsonr(asarray, np.asarray(re_predict_distance_score_metadata))[0]
        corr_matrix[2, idx] = pearsonr(asarray, np.asarray(continues_predict_distance_score_ocsvm))[0]
        corr_matrix[3, idx] = pearsonr(asarray, np.asarray(continues_predict_distance_score_metadata))[0]

    correlation_matrix = np.round(corr_matrix * 100) / 100

    fig, ax = plt.subplots()

    im, cbar = heatmap(corr_matrix, model_name, features, ax = ax, cmap = "coolwarm", cbarlabel = "Pearson product-moment")
    annotate_heatmap(im, valfmt = "{x:.1f} t")

    # fig.tight_layout()
    plt.show()
