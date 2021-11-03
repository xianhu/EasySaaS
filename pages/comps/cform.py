# _*_ coding: utf-8 _*_

"""
form of page
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(text_hd, text_sub, form, button, others):
    """
    layout of components
    """
    return [
        html.Div(text_hd, className="text-center fs-1"),
        html.Div(text_sub, className="text-center text-muted"),
        html.Div(form, className="mt-4"),
        html.Div(button, className="mt-4"),
        dbc.Row(children=[
            dbc.Col(others[0], width="auto"),
            dbc.Col(others[1], width="auto"),
        ], justify="between", class_name="mt-1"),
    ]
