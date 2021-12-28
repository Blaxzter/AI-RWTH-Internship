import pickle

import numpy as np
from plotly.subplots import make_subplots
import math
import plotly.graph_objects as go

if __name__ == '__main__':

    with open('data_features.pickle', 'rb') as handle:
        data_features = pickle.load(handle)
    with open('features.pickle', 'rb') as handle:
        features = pickle.load(handle)
    with open('metadata_model_prediction.pickle', 'rb') as handle:
        metadata_model_prediction = pickle.load(handle)

    for prediction, data_feature in zip(metadata_model_prediction, data_features):
        data_feature['prediction'] = prediction

    features.append('prediction')

    rows = int(math.ceil(len(features) / 2))
    fig = make_subplots(rows = rows, cols = 2, subplot_titles = features)

    idx = 0
    for i in range(2):
        for c in range(rows):
            try:
                feature = features[idx]
                feature_data = list(map(lambda x: x[feature], data_features))
                fig.add_trace(
                    go.Scatter(x = np.arange(len(feature_data)), y = feature_data),
                    row = c + 1, col = i + 1
                )
                idx += 1
            except IndexError:
                continue

    fig.show()
