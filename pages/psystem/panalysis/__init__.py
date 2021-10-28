# _*_ coding: utf-8 _*_

"""
page of analysis
"""

from app import app
from dash import html, Input, Output, State

import dash_bootstrap_components as dbc
from .catalog import layout_catalog

from dash import html

def layout(pathname, search):
    """
    layout of page
    """
    return html.Div([
        dbc.Row(children=[
            dbc.Col(dbc.Breadcrumb(items=[
                {"label": "Docs", "href": "/docs", "external_link": True},
                {"label": "Breadcrumb", "active": True},
            ])),
            dbc.Col(html.A(html.I(className="bi bi-list"), id="id-navbar1-toggler", n_clicks=0), width="auto", class_name="ms-auto"),
        ], class_name="gx-0 d-md-none d-lg-none px-3"),
        dbc.Container(children=[
            dbc.Collapse(layout_catalog(), id="id-navbar1-collapse", is_open=False, 
            className="d-md-block bg-light p-4 h-100 overflow-scroll side-class"),
            html.Div(html.Div("fesd", style={"height": "1000px"}), className="bg-warning w-100 overflow-scroll"),
        ], class_name="gx-0 d-flex flex-column flex-md-row h-100")
    ], className="h-100 overflow-scroll")


@app.callback(
    Output("id-navbar1-collapse", "is_open"),
    Input("id-navbar1-toggler", "n_clicks"),
    State("id-navbar1-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open