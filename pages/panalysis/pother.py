# _*_ coding: utf-8 _*_

"""
other page
"""

import dash_bootstrap_components as dbc


def layout(pathname, search):
    """
    layout of page
    """
    return dbc.Card(children=[
        dbc.CardHeader(dbc.Row(children=[
            dbc.Col("Other page", width="auto", class_name="fw-bold"),
            dbc.Col(dbc.Button("xxx", size="sm", class_name="invisible"), width="auto"),
        ], align="center", justify="between"), class_name="px-4 py-3"),
        dbc.Row(None, align="start", justify="start", class_name="p-4"),
    ], class_name="mt-2", style={"minHeight": "600px"})
