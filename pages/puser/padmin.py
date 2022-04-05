# _*_ coding: utf-8 _*_

"""
admin page
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        dbc.Card(children=[
            dbc.CardHeader("Admin", class_name="px-4 py-3"),
            html.Div(children=[], className="p-4"),
        ], class_name=None),
    ], className="mb-4")
