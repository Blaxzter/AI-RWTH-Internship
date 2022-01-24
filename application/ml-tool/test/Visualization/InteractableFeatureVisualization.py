import pickle

import dash
import numpy as np
import plotly.graph_objects as go
from dash import dcc
from dash import Dash, html, Input, Output, callback_context
from dash.dependencies import Input, Output
from scipy import signal
from sklearn.preprocessing import MinMaxScaler

current_figure = None

if __name__ == '__main__':
    with open('data/data_features.pickle', 'rb') as handle:
        data_features = pickle.load(handle)
    with open('data/features.pickle', 'rb') as handle:
        features = pickle.load(handle)
    with open('data/prediction.pickle', 'rb') as handle:
        predictions = pickle.load(handle)
    with open('data/re_predict_data.pickle', 'rb') as handle:
        re_predict_data = pickle.load(handle)

    with open('data/gram_matrix.pickle', 'rb') as handle:
        gram_matrix = np.asarray(pickle.load(handle))

    for idx, avg_gram_matrix in enumerate(np.average(np.asarray(gram_matrix), 0)):
        data_features[idx]['gram_matrix'] = avg_gram_matrix

    features.append('gram_matrix')

    for name in ['prediction', 'pred_confidence', 'distance_to_decision', 'outlier_probability']:
        predictions['path_ocsvm'][0][name] = 0
        predictions['meta_data_model'][0][name] = 0
        predictions['path_ocsvm'][1][name] = 0
        predictions['meta_data_model'][1][name] = 0

    re_prediction = {
        'meta_data_model': {data_name: re_predict_data['meta_data_model'][-1][idx] for idx, data_name in enumerate(['prediction', 'pred_confidence', 'distance_to_decision', 'outlier_probability'])},
        'path_ocsvm': {data_name: re_predict_data['path_ocsvm'][-1][idx] for idx, data_name in enumerate(['prediction', 'pred_confidence', 'distance_to_decision', 'outlier_probability'])}
    }

    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Markdown("# Meta data - Features"),
        dcc.Checklist(
            id = "selected_model",
            options = [{"label": 'Meta Data Model', "value": 'meta_data_model'},
                       {"label": 'Path OCSVM', "value": 'path_ocsvm'}],
            value = ['meta_data_model'],
            labelStyle = {'display': 'inline-block'}
        ),
        dcc.Graph(id = "line-chart"),
        dcc.Markdown("## Features"),
        dcc.Checklist(
            id = "features",
            options = [{"label": x, "value": x} for x in features],
            value = features[:1],
            labelStyle = {'display': 'inline-block'}
        ),
        dcc.Markdown("## Prediction data"),
        dcc.Checklist(
            id = "model_information",
            options = [
                {"label": 'prediction', "value": 'prediction'},
                {"label": 'distance_to_decision', "value": 'distance_to_decision'},
                {"label": 'pred_confidence', "value": 'pred_confidence'},
                {"label": 'outlier_probability', "value": 'outlier_probability'}],
            value = ['outlier_probability', 'pred_confidence'],
            labelStyle = {'display': 'inline-block'}
        ),
        dcc.Markdown("## Smoothing"),
        dcc.Checklist(
            id = "post_process",
            options = [{"label": 'scaling', "value": 'scaling'}, {"label": 'smoothing', "value": 'smoothing'}],
            value = ['scaling', 'smoothing'],
            labelStyle = {'display': 'inline-block'}
        ),
        dcc.Input(
            id = "number_smoothing",
            type = "number",
            value = 53,
            placeholder = "input type {}".format("number"),
            step = 2,
            min = 1,
        ),
        dcc.Input(
            id = "number_polynomial",
            type = "number",
            value = 3,
            placeholder = "input type {}".format("number"),
        ),
        dcc.Checklist(
            id = "data_origin",
            options = [{"label": 'continues', 'value': 'continues'}, {"label": 'retrained', 'value': 'retrained'}],
            value = ['continues'],
            labelStyle = {'display': 'inline-block'}
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
            value = len(data_features),
            placeholder = "input type {}".format("number"),
        ),
        html.Button('Export', id = 'export_button', n_clicks = 0),
        html.Div(id = 'container-button-timestamp')
    ])

    label_mapping = {
        "amount": "Files per Backup (amount)",
        "path_ocsvm outlier_probability": "OCSVM: Outlier Probability",
        "meta_data_model outlier_probability": "Metadata: Outlier Probability",
        "meta_data_model pred_confidence": "Metadata: Prediction Confidence",
        "continues meta_data_model pred_confidence": "Continues Metadata: Prediction Confidence",
        "repredict meta_data_model pred_confidence": "Repredict OCSVM: Prediction Confidence",
        "meta_data_model prediction": "Metadata: Positive Prediction",
    }

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
            img_bytes = current_figure.to_image(format = "pdf", width = 1200, height = 600, scale = 2)
            f = open("exported_img.pdf", "wb")
            f.write(img_bytes)
            f.close()

        return html.Div("Exported")

    @app.callback(
        Output("line-chart", "figure"),
        [
            Input("selected_model", "value"),
            Input("features", "value"),
            Input("model_information", "value"),
            Input("number_smoothing", "value"),
            Input("number_polynomial", "value"),
            Input("post_process", "value"),
            Input("data_origin", "value")
        ]
    )
    def update_line_chart(c_model, c_features, model_information, number_smoothing, number_polynomial, post_process, data_origins):
        fig = go.Figure()

        for feature in c_features:
            feature_data = list(map(lambda x: x[feature], data_features))

            plot_data = feature_data

            if 'smoothing' in post_process:
                plot_data = signal.savgol_filter(plot_data, number_smoothing, number_polynomial)

            if 'scaling' in post_process:
                plot_data = MinMaxScaler(
                    feature_range = (0, 1) if np.min(feature_data) >= 0 else (-1, 1)
                ).fit_transform(np.asarray(plot_data).reshape(len(plot_data), 1)).reshape(1, -1)[0]

            label_name = label_mapping[feature] if feature in list(label_mapping.keys()) else feature

            fig.add_trace(
                go.Scatter(x = np.arange(len(feature_data)), y = plot_data, name = label_name, mode='lines+markers'),
            )

        for data_origin in data_origins:
            for model in c_model:
                for info in model_information:

                    if 'continues' == data_origin:
                        model_prediction = list(map(lambda x: x[info], predictions[model]))

                    if 'retrained' == data_origin:
                        model_prediction = re_prediction[model][info]

                    if 'smoothing' in post_process:
                        model_prediction = signal.savgol_filter(model_prediction, number_smoothing, number_polynomial)

                    if 'scaling' in post_process:
                        model_prediction = MinMaxScaler().fit_transform(
                            np.asarray(model_prediction).reshape(len(model_prediction), 1)).reshape(1, -1)[0]

                    label_name = label_mapping[f'{data_origin} {model} {info}'] if f'{data_origin} {model} {info}' in list(label_mapping.keys()) else f'{data_origin} {model} {info}'

                    if 'prediction' == info:
                        data_range = np.arange(len(model_prediction))
                        data_range[np.where(np.asarray(model_prediction) == 0)] = -1
                        fig.add_trace(
                            go.Scatter(
                                x = data_range,
                                y = model_prediction,
                                name = label_name,
                                mode='markers',
                                marker=dict(size=10, symbol = 'diamond')
                            )
                        )
                    else:
                        fig.add_trace(
                            go.Scatter(x = np.arange(len(model_prediction)), y = model_prediction, name = label_name, mode='lines')
                        )

        fig.update_layout(legend = dict(
            orientation = "h",
            yanchor = "bottom",
            y = 1.02,
            xanchor = "right",
            x = 1
        ))
        fig.layout.uirevision = True

        global current_figure
        current_figure = fig

        fig.update_xaxes(title_text = 'Index of Backups')
        fig.update_yaxes(title_text = 'Scaled Value')

        return fig


    app.run_server(debug = True, port = 5052)
