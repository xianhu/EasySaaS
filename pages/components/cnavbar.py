# _*_ coding: utf-8 _*_

"""
navbar of page
"""

import dash
import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from config import config_app_name

from ..paths import *


def layout(pathname, search, fluid=None, class_container=None, class_navbar=None):
    """
    layout of component
    """
    # define components
    class_navlink = "fw-bold text-center border-bottom mx-md-1 p-md-3"
    nav_link_list = [
        dbc.NavLink("Intros", href=PATH_INTROS, class_name=class_navlink),
        dbc.NavLink("Analysis", href=PATH_ANALYSIS, class_name=class_navlink),
    ]

    # define components
    nav_item_list = dbc.NavItem(children=[
        html.A("Sign up", href=PATH_REGISTERE, className=None),
        dbc.Button("Sign in", href=PATH_LOGIN, color="primary", outline=True, class_name="fw-bold ms-3"),
    ] if not flask_login.current_user.is_authenticated else [
        html.A(html.I(className="bi bi-bell fs-5"), href=PATH_USER, className=None),
        html.A(html.I(className="bi bi-person-circle fs-4"), href=PATH_USER, className="ms-3"),
    ], class_name="d-flex flex-row align-items-center justify-content-center py-1")

    # return result
    class_navbar = class_navbar or "bg-primary border-bottom py-0"
    return dbc.Navbar(dbc.Container(children=[
        dbc.NavbarBrand(children=[
            html.Img(src=dash.get_asset_url("favicon.svg"), style={"width": "1.2rem"}),
            html.Span(config_app_name, className="fs-5 align-middle ms-1"),
        ], href=PATH_INTROS),
        dbc.NavbarToggler(id="id-toggler", class_name="my-2"),
        dbc.Collapse(children=[
            dbc.Nav(nav_link_list, navbar=True, class_name="mx-auto"),
            dbc.Nav(nav_item_list, navbar=True, class_name=None),
        ], id="id-collapse", is_open=False, navbar=True),
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
