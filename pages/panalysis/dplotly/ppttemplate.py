# _*_ coding: utf-8 _*_

"""
template page
"""

import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, dcc, html

from app import app

TAG = "analysis-plotly-template"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return dbc.Card(children=[
        dbc.CardHeader("Charts Template", class_name="px-4 py-3"),
        html.Div(dbc.Spinner(id=f"id-{TAG}-content"), className="p-4"),
    ], class_name=None, style={"minHeight": "600px"})


@app.callback(
    Output(f"id-{TAG}-content", "children"),
    Input(f"id-{TAG}-content", "type"),
    prevent_initial_call=False,
)
def _init_page(spinner_type):
    # define variables
    random_x = np.linspace(0, 1, 100)
    random_y0 = np.random.randn(100) + 5
    random_y1 = np.random.randn(100)
    random_y2 = np.random.randn(100) - 5

    # define components
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=random_x, y=random_y0, mode="markers", name="markers"))
    figure.add_trace(go.Scatter(x=random_x, y=random_y1, mode="lines+markers", name="lines+markers"))
    figure.add_trace(go.Scatter(x=random_x, y=random_y2, mode="lines", name="lines"))

    # return result
    return dcc.Graph(figure=figure, className=None)
