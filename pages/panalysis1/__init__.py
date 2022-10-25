# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return dbc.Card(children=[
        dbc.CardBody(dbc.Spinner(html.Div("Analysis1 Page"))),
    ], class_name=None, style={"minHeight": "400px"})
