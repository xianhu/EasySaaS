# _*_ coding: utf-8 _*_

"""
other page
"""

from dash import html
import dash_bootstrap_components as dbc


def layout(pathname, search):
    """
    layout of page
    """
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col("Other page", width="auto", class_name="fw-bold"),
            dbc.Col(dbc.Button("xxx", size="sm", class_name="invisible"), width="auto"),
        ], align="center", justify="between", class_name="border-bottom w-100 mx-auto px-3 py-2"),
        dbc.Row(dbc.Col(children=[
            html.H6("format 111"),
            html.Div("format 222", className="px-2"),
            html.Div("format 333", className="px-2"),
        ], width="auto"), align="start", justify="start", class_name="w-100 mx-auto px-3 py-3"),
    ], style={"minHeight": "600px"})
