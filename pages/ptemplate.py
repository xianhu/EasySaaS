# _*_ coding: utf-8 _*_

"""
template page
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return dbc.Card(children=[
        dbc.CardHeader("Template Page", class_name="px-4 py-3"),
        dbc.Spinner(html.Div(children=None, className="p-4")),
    ], class_name=None, style={"minHeight": "600px"})
