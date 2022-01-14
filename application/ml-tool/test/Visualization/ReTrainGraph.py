import pickle

import dash
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

if __name__ == '__main__':
    with open('re_predict_data.pickle', 'rb') as handle:
        re_predict_data = pickle.load(handle)

    model_names = list(re_predict_data.keys())

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.P("Meta data - Features"),
        dcc.Graph(id="line-chart"),
        dcc.Slider(
            id='my-slider',
            min=0,
            max=len(list(re_predict_data.values())[0]),
            step=1,
            value=0,
            tooltip = {"placement": "bottom", "always_visible": True},
        ),
    ])

    @app.callback(
        Output("line-chart", "figure"),
        [Input("my-slider", "value")])
    def update_line_chart(slider_value):
        fig = go.Figure()
        for model_name, model_data in re_predict_data.items():
            feature_data = list(map(lambda y: y[slider_value], filter(lambda x: len(x) > slider_value, model_data)))
            fig.add_trace(
                go.Scatter(x = np.arange(len(feature_data)), y = feature_data, name=model_name),
            )

        return fig

    app.run_server(debug=True, port=8051)
