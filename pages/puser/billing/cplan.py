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
    # define components
    plan_price = html.Div("$29/m", className="fw-bold")
    plan_info = [
        html.Div("Basic Plan", className=None),
        html.Div("Next payment: 03/03/2021", className="text-muted"),
    ]

    # return result
    return dbc.Card(children=[
        dbc.Row(children=[
            dbc.Col("Current Plan:", width="auto"),
            dbc.Col(dbc.Button("Change", id=f"id-{TAG}-change"), width="auto"),
        ], align="center", justify="between", class_name="gx-0 border-bottom px-4 py-3"),
        dbc.Row(children=[
            dbc.Col(plan_info, width="auto"),
            dbc.Col(plan_price, width="auto"),
        ], align="center", justify="between", class_name="px-4 py-4"),
        dbc.Row(dbc.Col(children=[
            dbc.Button("Renewal Fee", id=f"id-{TAG}-renewal", class_name="w-100"),
        ], width=12, md=4), class_name="px-4 pb-4"),
    ], class_name="mb-4")
