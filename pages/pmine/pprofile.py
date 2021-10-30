# _*_ coding: utf-8 _*_

"""
page of profile
"""

from app import app
import dash_bootstrap_components as dbc
from dash import html, Output, Input, State

TAG = "profile"


def layout(pathname, search):
    """
    layout of page
    """
    class_li = "fw-bold text-muted cursor-pt hover-primary my-2"
    catalog = html.Div(children=[
        dbc.Row(children=[
            dbc.Col("Profile", id="id-catalog", width="auto"),
            dbc.Col(dbc.NavbarToggler(html.A(html.I(className="bi bi-list fs-1")), id=f"id-aa-toggler", class_name="border"), width="auto"),
        ], align="center", justify="between", class_name="gx-0 d-md-none fw-bold text-muted"),
        dbc.Collapse(children=[
            html.Ul(children=[
                html.Li("Profile", id="id-profile", className=class_li),
                html.Li("Account", id="id-account", className=class_li),
                html.Li("Upgrade", id="id-upgrade", className=class_li),
            ], className=""),
            dbc.Button("Logout", className="w-100"),
        ], id="id-aa-collapse", is_open=False, class_name="d-md-block")
    ], className="side-class d-md-block bg-light px-3 py-2 border-bottom")

    return dbc.Container(children=[
        catalog,
        dbc.Container("111")
    ],class_name="gx-0 d-flex flex-column flex-md-row h-100")

    return dbc.Row(children=[
        dbc.Col(catalog, width=12, md=2, class_name="bg-light p-4"),
        dbc.Col("11111", width=12, md=10),
    ], class_name="gx-0 h-100")


@app.callback(
    Output("id-aa-collapse", "is_open"),
    Input("id-aa-toggler", "n_clicks"),
    State("id-aa-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
