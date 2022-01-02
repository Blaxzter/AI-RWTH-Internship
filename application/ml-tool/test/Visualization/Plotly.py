import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

if __name__ == '__main__':

    x = np.arange(10)
    fig = make_subplots(rows = 1, cols = 2)

    fig.add_trace(
        go.Scatter(x = x, y = x ** 2),
        row = 1, col = 1
    )
    # Edit the layout
    fig.update_layout(title = 'Average High and Low Temperatures in New York',
                      xaxis_title = 'Month',
                      yaxis_title = 'Temperature (degrees F)')
    fig.show()
