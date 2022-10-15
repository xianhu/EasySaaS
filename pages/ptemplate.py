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
        # dbc.CardHeader("Template Page", class_name="px-4 py-3"),
        dbc.CardBody(dbc.Spinner(html.Div("Template Page"))),
    ], class_name=None, style={"minHeight": "400px"})
