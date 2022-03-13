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
        dbc.CardHeader("Other Page", class_name="px-4 py-3"),
        dbc.Row(align="start", justify="start", class_name="p-4"),
    ], class_name=None, style={"minHeight": "600px"})
