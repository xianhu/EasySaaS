# _*_ coding: utf-8 _*_

"""
page of desc
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search):
    """
    layout of page
    """
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col("format description", width="auto", class_name="fw-bold"),
            dbc.Col(dbc.Button("Download file", color="primary", outline=True, size="sm"), width="auto"),
        ], align="center", justify="between", class_name="border-bottom mx-auto px-3 py-2"),
        dbc.Row(dbc.Col(children=[
            html.H6("format 111"),
            html.Div("format 111", className="px-2"),
            html.Div("format 111", className="px-2"),

            html.H6("format 111", className="mt-3"),
            html.Div("format 111", className="px-2"),
            html.Div("format 111", className="px-2"),

            html.H6("format 111", className="mt-3"),
            html.Div("format 111", className="px-2"),
            html.Div("format 111", className="px-2"),
        ]), class_name="mx-auto px-3 py-3"),
    ], className="bg-white h-75 border")
