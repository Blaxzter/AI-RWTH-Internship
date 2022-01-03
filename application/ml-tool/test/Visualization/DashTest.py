import pickle

import dash
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

if __name__ == '__main__':
    with open('data_features.pickle', 'rb') as handle:
        data_features = pickle.load(handle)
    with open('features.pickle', 'rb') as handle:
        features = pickle.load(handle)
    with open('metadata_model_prediction.pickle', 'rb') as handle:
        metadata_model_prediction = pickle.load(handle)

    for prediction, data_feature in zip(metadata_model_prediction, data_features):
        data_feature['prediction'] = prediction if prediction is not None else None

    features.append('prediction')

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.P("Meta data - Features"),
        dcc.Graph(id="line-chart"),
        dcc.Checklist(
            id = "checklist",
            options = [{"label": x, "value": x}
                       for x in features],
            value = features[:3],
            labelStyle = {'display': 'inline-block'}
        ),
    ])

    @app.callback(
        Output("line-chart", "figure"),
        [Input("checklist", "value")])
    def update_line_chart(c_features):
        fig = go.Figure()
        for feature in c_features:
            feature_data = list(map(lambda x: x[feature], data_features))
            fig.add_trace(
                go.Scatter(x = np.arange(len(feature_data)), y = feature_data, name=feature),
            )

        return fig

    app.run_server(debug=True)
