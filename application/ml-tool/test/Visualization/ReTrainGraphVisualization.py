import pickle

import dash
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from collections import defaultdict

from scipy import signal
from sklearn.preprocessing import MinMaxScaler

current_figure = None

if __name__ == '__main__':
    with open('data/re_predict_data.pickle', 'rb') as handle:
        re_predict_data = pickle.load(handle)

    with open('data/data_features.pickle', 'rb') as handle:
        data_features = pickle.load(handle)

    amount_features = feature_data = list(map(lambda x: x['amount'], data_features))

    model_names = list(re_predict_data.keys())

    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.P("Meta data - Features"),
        dcc.Graph(id="line-chart"),
        dcc.Checklist(
            id = "selected_model",
            options = [{"label": 'Meta Data Model', "value": 'meta_data_model'},
                       {"label": 'Path OCSVM', "value": 'path_ocsvm'}],
            value = ['meta_data_model'],
            labelStyle = {'display': 'inline-block'}
        ),
        dcc.Checklist(
            id = "show_amount",
            options = [{"label": 'Show Amount', "value": 'amount'}],
            value = ['amount'],
            labelStyle = {'display': 'inline-block'}
        ),
        dcc.Slider(
            id='my-slider',
            min=0,
            max=len(list(re_predict_data.values())[0]),
            step=1,
            value=0,
            tooltip = {"placement": "bottom", "always_visible": True},
        ),

        dcc.Markdown("## Export"),
        dcc.Input(
            id = "export_start",
            type = "number",
            value = 0,
            placeholder = "input type {}".format("number"),
        ),
        dcc.Input(
            id = "export_end",
            type = "number",
            value = len(re_predict_data['meta_data_model']),
            placeholder = "input type {}".format("number"),
        ),
        html.Button('Export', id = 'export_button', n_clicks = 0),
        html.Div(id = 'container-button-timestamp')
    ])

    @app.callback(
        Output('container-button-timestamp', 'children'),
        Input('export_button', 'n_clicks'),
        Input('export_start', 'value'),
        Input('export_end', 'value')
    )
    def displayClick(btn1, export_start, export_end):
        global current_figure
        if current_figure is not None:
            current_figure.update_xaxes(range = [export_start, export_end])
            img_bytes = current_figure.to_image(format = "pdf", width = 1200, height = 400, scale = 2)
            f = open("re_exported_img.pdf", "wb")
            f.write(img_bytes)
            f.close()

        return html.Div("Exported")

    @app.callback(
        Output("line-chart", "figure"),
        [Input("selected_model", "value"), Input("my-slider", "value"), Input("show_amount", "value"), ])
    def update_line_chart(selected_model, slider_value, show_amount):
        fig = go.Figure()
        data = defaultdict(dict)

        for model_name in selected_model:
            model_data = re_predict_data[model_name]
            for i, data_name in enumerate(['prediction', 'confidence', 'desc_boundary', 'outlier_probability']):
                c_data = list(map(lambda x: x[i][slider_value], filter(lambda z: len(z[0]) > slider_value, model_data)))
                data[model_name][data_name] = c_data

        for model_name, model_data in data.items():
            for information_name, view_data in model_data.items():

                if 'desc_boundary' in information_name:
                    view_data = MinMaxScaler(
                        # feature_range = (0, 1) if np.min(view_data) >= 0 else (-1, 1)
                    ).fit_transform(np.asarray(view_data).reshape(len(view_data), 1)).reshape(1, -1)[0]

                if 'prediction' == information_name:
                    data_range = np.arange(len(view_data))
                    # data_range[np.where(np.asarray(view_data) == 0)] = -1
                    fig.add_trace(
                        go.Scatter(
                            x = data_range,
                            y = view_data,
                            name = 'Prediction',
                            mode='markers',
                            marker=dict(size=5, symbol = 'diamond')
                        )
                    )
                else:

                    view_data = signal.savgol_filter(view_data, 3, 1)
                    fig.add_trace(
                        go.Scatter(x = np.arange(len(view_data)), y = view_data, name = f'{model_name} {information_name}', mode='lines')
                    )

        if 'amount' in show_amount:
            view_data = signal.savgol_filter(amount_features, 21, 3)
            view_data = MinMaxScaler(
                # feature_range = (0, 1) if np.min(view_data) >= 0 else (-1, 1)
            ).fit_transform(np.asarray(view_data).reshape(len(view_data), 1)).reshape(1, -1)[0]
            fig.add_trace(
                go.Scatter(x = np.arange(len(view_data)), y = view_data, name = f'Files per backup',
                           mode = 'lines')
            )

        fig.update_layout(legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 1
        ))
        fig.layout.uirevision = True

        fig.update_xaxes(title_text = 'Index of Backups')
        fig.update_yaxes(title_text = 'Scaled Value')

        global current_figure
        current_figure = fig

        return fig

    app.run_server(debug=True, port=8051)
