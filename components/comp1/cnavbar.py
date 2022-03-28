# _*_ coding: utf-8 _*_

"""
navbar component
"""

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, html

from paths import *
from . import cbrand


def layout(pathname, search, fluid=None, class_container=None, class_navbar=None):
    """
    layout of component
    """
    # define components
    class_link = "fw-bold text-center border-bottom mx-md-1 p-md-3"
    nav_links = dbc.Nav(children=[
        dbc.NavLink("Intros", href=PATH_INTROS, class_name=class_link),
        dbc.NavLink("Analysis", href=PATH_ANALYSIS, class_name=class_link),
    ], navbar=True, class_name="mx-auto")

    # define components
    args = {"color": "primary", "outline": True}
    nav_right = dbc.Nav(dbc.NavItem(children=[
        html.A("Sign up", href=PATH_REGISTERE, className=None),
        dbc.Button("Sign in", href=PATH_LOGIN, **args, class_name="fw-bold ms-3"),
    ] if not flask_login.current_user.is_authenticated else [
        html.A(html.I(className="bi bi-bell fs-5"), href=PATH_USER, className=None),
        html.A(html.I(className="bi bi-person-circle fs-4"), href=PATH_USER, className="ms-3"),
    ], class_name="d-flex align-items-center justify-content-center py-1"), navbar=True)

    # return result
    class_navbar = class_navbar or "border-bottom py-0"
    return dbc.Navbar(dbc.Container(children=[
        cbrand.layout(pathname, search, href=PATH_ROOT),
        dbc.NavbarToggler(id="id-toggler", class_name="my-2"),
        dbc.Collapse([nav_links, nav_right], id="id-collapse", navbar=True),
    ], fluid=fluid, class_name=class_container), class_name=class_navbar)


@dash.callback(
    Output("id-collapse", "is_open"),
    Input("id-toggler", "n_clicks"),
    State("id-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
