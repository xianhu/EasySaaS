# _*_ coding: utf-8 _*_

"""
Current Plan
"""

import dash_bootstrap_components as dbc
from dash import html

TAG = "user-plan"


def layout(pathname, search):
    """
    layout of card
    """
    return dbc.Card(children=[
        dbc.Row(children=[
            dbc.Col("Current Plan:", width="auto"),
            dbc.Col(dbc.Button("Change", id=f"id-{TAG}-change"), width="auto"),
        ], align="center", justify="between", class_name="border-bottom gx-0 px-4 py-3"),
        dbc.Row(children=[
            dbc.Col(children=[
                html.Div("Basic Plan", className=None),
                html.Div("Next payment: 10/12/2022", className="text-muted"),
            ], width=9),
            dbc.Col(children=[
                html.Div("$29/m", className="fw-bold"),
            ], width=3, class_name="text-end"),
            # change line
            dbc.Col(children=[
                dbc.Button("Renewal Fee", id=f"id-{TAG}-renewal", class_name="w-100"),
            ], width=12, md=4, class_name="mt-4 mt-md-4"),
        ], align="center", class_name="p-4"),
    ], class_name="mb-4")
