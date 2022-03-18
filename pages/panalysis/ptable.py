# _*_ coding: utf-8 _*_

"""
table page
"""

import dash_bootstrap_components as dbc
from dash import html

TAG = "analysis-table"


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    args = {"size": "sm", "color": "primary", "outline": True}
    button = dbc.Button("Download File", id=f"id-{TAG}-button", **args)

    # define components
    row_header = dbc.Row(children=[
        dbc.Col("Table Page", width="auto"),
        dbc.Col(button, width="auto"),
    ], align="center", justify="between")

    # return result
    return dbc.Card(children=[
        dbc.CardHeader(row_header, class_name="px-4 py-3"),
        html.Div(None, className="p-4"),
    ], class_name=None, style={"minHeight": "600px"})
