# _*_ coding: utf-8 _*_

"""
plotly table page
"""

import dash_bootstrap_components as dbc
import plotly
import plotly.graph_objects as go
from dash import Input, Output, dcc, html

from app import app

TAG = "analysis-tables-plotly"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return dbc.Card(children=[
        dbc.CardHeader("Plotly Table", class_name="px-4 py-3"),
        dbc.Spinner(html.Div(id=f"id-{TAG}-content", className="p-4")),
    ], class_name=None, style={"minHeight": "600px"})


@app.callback(
    Output(f"id-{TAG}-content", "children"),
    Input(f"id-{TAG}-content", "className"),
    prevent_initial_call=False,
)
def _init_page(n_clicks):
    data = plotly.data.iris()
    return dcc.Graph(figure=go.Figure(go.Table(
        header=dict(values=list(data.columns), fill_color="paleturquoise", align="left"),
        cells=dict(values=[data[c] for c in data.columns], fill_color="lavender", align="left"),
    ), layout=None), className=None)
