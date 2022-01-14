import pickle

import plotly.graph_objects as go

if __name__ == '__main__':
    with open('re_predict_data.pickle', 'rb') as handle:
        re_predict_data = pickle.load(handle)

    fig = go.Figure(
        data = [go.Scatter(x = [0, 1], y = [0, 1], name = 'meta_data_model'),
                go.Scatter(x = [0, 1], y = [0, 1], name = 'path_ocsvm')],
        layout = go.Layout(
            xaxis = dict(autorange = True),
            yaxis = dict(autorange = True),
            title = "Start Title",
            updatemenus = [dict(
                type = "buttons",
                buttons = [dict(label = "Play",
                                method = "animate",
                                args = [None, {"frame": {"duration": 50,
                                                         "redraw": True},
                                               "fromcurrent": True,
                                               "transition": {"duration": 50}}])])]
        ),
        frames = [
            go.Frame(
                data = [
                    go.Scatter(x = list(range(len(a))), y = a, name = 'meta_data_model'),
                    go.Scatter(x = list(range(len(b))), y = b, name = 'path_ocsvm')
                ]) for a, b in list(zip(re_predict_data['meta_data_model'], re_predict_data['path_ocsvm']))
        ]
    )

    fig.show()
