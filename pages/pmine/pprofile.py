# _*_ coding: utf-8 _*_

"""
page of profile
"""

from dash import html
import dash_bootstrap_components as dbc


def layout(pathname, search):
    """
    layout of page
    """
    form = dbc.Form(children=[
        dbc.Row(children=[
            dbc.Label("username:", html_for="example-email-row", width=4),
            dbc.Col(dbc.Input(type="text", id="example-email-row",), width=8),
        ], className="mb-3"),
        dbc.Row(children=[
            dbc.Label("phone:", html_for="example-email-row", width=4),
            dbc.Col(dbc.Input(type="tel", id="",), width=8),
        ], className="mb-3"),
        dbc.Button("Save", class_name="w-50")
    ], class_name="p-4 border rounded bg-light")
    form1 = dbc.Form(children=[
        dbc.Row(children=[
            dbc.Label("Password:", html_for="example-email-row", width=4),
            dbc.Col(dbc.Input(type="password", id="example-email-row",), width=8),
        ], className="mb-3"),
        dbc.Row(children=[
            dbc.Label("Confirm:", html_for="example-email-row", width=4),
            dbc.Col(dbc.Input(type="password", id="",), width=8),
        ], className="mb-3"),
        dbc.Button("Update", class_name="w-50")
    ], class_name="p-4 border rounded bg-light")
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col(form, width=12, md=4, class_name="mt-2"),
            dbc.Col(form1, width=12, md=4, class_name="mt-2"),
        ], justify="", class_name="")
    ], className="w-100 p-4 h-100 overflow-scroll")
