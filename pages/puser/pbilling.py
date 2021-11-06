# _*_ coding: utf-8 _*_

"""
page of plan and billing
"""

import dash_bootstrap_components as dbc
from dash import html

TAG = "user-billing"


def layout(pathname, search):
    """
    layout of page
    """
    card1 = dbc.Card(children=[
        dbc.Row(children=[
            dbc.Col("Current Plan:", width="auto"),
            dbc.Col(dbc.Button("Change", id=f"id-{TAG}-button"), width="auto"),
        ], align="center", justify="between", class_name="border-bottom p-4 gx-0"),
        dbc.Row(children=[
            dbc.Col(children=[
                "Basic Plan",
                html.Div("Next payment on 03/03/2021", className="text-muted"),
            ], width="auto"),
            dbc.Col(html.Div("$29/mo", className="fw-bold"), width="auto"),
        ], align="center", justify="between", class_name="p-4"),
        dbc.Row(dbc.Col(children=[
            dbc.Button("Renewal Fee", id=f"id-{TAG}-button", class_name="w-100"),
        ], width=12, md=4), class_name="p-4"),
    ], class_name="mb-4")

    card2 = dbc.Card(children=[
        html.Div("Invoice History:", className="border-bottom p-4"),
        dbc.Row(children=[
            dbc.Col(children=[
                html.A("Invoice #91240", href="#"),
                html.Div("Billed 01/12/2020", className="text-muted"),
            ], width="auto"),
            dbc.Col(dbc.Button("pay now", size="sm", outline=True, color="primary"), width="auto"),
        ], align="center", justify="between", class_name="p-4"),
        html.Hr(className="text-muted mx-4"),
        dbc.Row(children=[
            dbc.Col(children=[
                html.A("Invoice #91240", href="#"),
                html.Div("Billed 01/10/2020", className="text-muted"),
            ], width="auto"),
            dbc.Col(dbc.Button("paid", size="sm", outline=True, color="primary", disabled=True), width="auto"),
        ], align="center", justify="between", class_name="p-4"),
        html.Hr(className="text-muted mx-4"),
        dbc.Row(children=[
            dbc.Col(children=[
                html.A("Invoice #91240", href="#"),
                html.Div("Billed 01/08/2020", className="text-muted"),
            ], width="auto"),
            dbc.Col(dbc.Button("paid", size="sm", outline=True, color="primary", disabled=True), width="auto"),
        ], align="center", justify="between", class_name="p-4"),
    ], class_name="mb-4")
    return [card1, card2]
