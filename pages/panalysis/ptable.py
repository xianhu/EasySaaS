# _*_ coding: utf-8 _*_

"""
table page
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    content = html.Div(children=[
        html.H6("format 111"),
        html.Div("format 222", className="px-2"),
        html.Div("format 333", className="px-2"),
    ])

    # return result
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col("File name: xxx.csv", width="auto", class_name="fw-bold"),
            dbc.Col(dbc.Button("Download file", size="sm", color="primary", outline=True), width="auto"),
        ], align="center", justify="between", class_name="border-bottom w-100 mx-auto px-3 py-2"),
        dbc.Row(dbc.Col(content, width="auto"), align="start", justify="start", class_name="w-100 mx-auto p-3"),
    ], style={"min-height": "600px"})
