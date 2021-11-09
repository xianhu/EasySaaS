# _*_ coding: utf-8 _*_

"""
Invoice History
"""

import dash_bootstrap_components as dbc
from dash import html

TAG = "user-invoice"


def layout(pathname, search):
    """
    layout of card
    """
    return dbc.Card(children=[
        html.Div("Invoice History:", className="border-bottom p-4"),
        dbc.Row(children=[
            dbc.Col(children=[
                html.A("Invoice #91240", href="#"),
                html.Div("Billed 01/12/2020", className="small text-muted"),
            ], width="auto"),
            dbc.Col(dbc.Button("pay now", size="sm", outline=True, color="primary"), width="auto"),
        ], align="center", justify="between", class_name="p-4"),
        html.Hr(className="text-muted mx-4 my-0"),
        dbc.Row(children=[
            dbc.Col(children=[
                html.A("Invoice #91230", href="#"),
                html.Div("Billed 01/10/2020", className="small text-muted"),
            ], width="auto"),
            dbc.Col(dbc.Button("paid", size="sm", outline=True, color="primary", disabled=True), width="auto"),
        ], align="center", justify="between", class_name="p-4"),
        html.Hr(className="text-muted mx-4 my-0"),
        dbc.Row(children=[
            dbc.Col(children=[
                html.A("Invoice #91220", href="#"),
                html.Div("Billed 01/08/2020", className="small text-muted"),
            ], width="auto"),
            dbc.Col(dbc.Button("paid", size="sm", outline=True, color="primary", disabled=True), width="auto"),
        ], align="center", justify="between", class_name="p-4"),
    ], class_name="mb-4")
