# _*_ coding: utf-8 _*_

"""
Current Plan
"""

from dash import html
import dash_bootstrap_components as dbc

TAG = "user-plan"


def layout(pathname, search):
    """
    layout of card
    """
    return dbc.Card(children=[
        dbc.Row(children=[
            dbc.Col("Current Plan:", width="auto"),
            dbc.Col(dbc.Button("Renewal", id=f"id-{TAG}-renewal"), width="auto"),
        ], align="center", justify="between", class_name="gx-0 border-bottom px-4 py-3"),
        dbc.Row(children=[
            dbc.Col(children=[
                html.Div("Basic Plan ($19/m)", className=None),
                html.Div("Next payment: 10/12/2022", className="text-muted"),
            ], width="auto", class_name=None),
            dbc.Col(dbc.Button("Change", id=f"id-{TAG}-change"), width="auto"),
        ], align="center", justify="between", class_name="p-4"),
    ], class_name="mb-4")
