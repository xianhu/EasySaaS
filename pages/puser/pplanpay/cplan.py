# _*_ coding: utf-8 _*_

"""
Current Plan
"""

import dash_bootstrap_components as dbc
from dash import html

TAG = "user-planpay-plan"


def layout(class_name=None):
    """
    layout of component
    """
    # define components
    left = [
        html.Div("Basic Plan ($19/m)", className=None),
        html.Div("Next payment: 10/12/2022", className="text-muted"),
    ]
    right = dbc.Button("Renewal or Change", id=f"id-{TAG}-change")

    # return result
    return dbc.Card(children=[
        dbc.CardHeader("Current Plan:", class_name="px-4 py-3"),
        dbc.Row(children=[
            dbc.Col(left, width="auto", class_name=None),
            dbc.Col(right, width="auto", class_name=None),
        ], align="center", justify="between", class_name="p-4"),
    ], class_name=class_name)
