# _*_ coding: utf-8 _*_

"""
plotly basic page
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

from . import cplotly


def layout(pathname, search):
    """
    layout of page
    """
    return dbc.Card(children=[
        dbc.CardHeader("Plotly Basic Page", class_name="px-4 py-3"),
        html.Div(dcc.Graph(figure=cplotly.fig_scatter), className="p-0"),
    ], class_name=None, style={"minHeight": "600px"})
