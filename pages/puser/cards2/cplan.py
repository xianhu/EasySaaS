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
        ], align="center", justify="between", class_name="gx-0 border-bottom px-4 py-3"),
        dbc.Row(children=[
            dbc.Col(children=[
                html.Div("Basic Plan"),
                html.Div("Next payment: 03/03/2021", className="text-muted"),
            ], width="auto"),
            dbc.Col("$29/m", width="auto", class_name="fw-bold"),
        ], align="center", justify="between", class_name="px-4 pt-4"),
        dbc.Row(dbc.Col(children=[
            dbc.Button("Renewal Fee", id=f"id-{TAG}-renewal", class_name="w-100"),
        ], width=12, md=4), class_name="p-4"),
    ], class_name="mb-4")
