# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc

TAG = "analysis1"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return dbc.Row(children=[
        dbc.Col(children=[], width=12, md=2, class_name="bg-primary h-100-scroll-md"),
        dbc.Col(children=[], width=12, md=10, class_name="bg-light p-4 h-100-scroll"),
    ], align="start", justify="center", class_name="mx-0 vh-100 overflow-auto")
