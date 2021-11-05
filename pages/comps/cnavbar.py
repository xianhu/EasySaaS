# _*_ coding: utf-8 _*_

"""
navbar of page
"""

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app
from config import config_app_name

from ..paths import *


def layout(pathname, search, fluid=None):
    """
    layout of components
    """
    # define components
    class_navlink = "fw-bold mx-auto mx-md-4 hover-primary"
    nav_link_list = [
        dbc.NavLink("Intros", href=PATH_INTROS, class_name=class_navlink),
        dbc.NavLink("Analysis", href=PATH_ANALYSIS, class_name=class_navlink),
    ]

    # define components
    class_navitem = "fw-bold mx-auto mx-md-0 d-flex align-items-center"
    if not flask_login.current_user.is_authenticated:
        args_button = {"outline": True, "color": "primary"}
        nav_item_list = dbc.NavItem([
            html.A("Sign up", href=PATH_REGISTERE, className="fw-bold"),
            dbc.Button("Sign in", href=PATH_LOGIN, **args_button, className="fw-bold ms-3"),
        ], class_name=class_navitem)
    else:
        class_icon = "fw-bold mx-0 text-secondary hover-primary"
        nav_item_list = dbc.NavItem([
            html.A(html.I(className="bi bi-bell fs-5 " + class_icon), href=f"{PATH_USER}-notify"),
            html.A(html.I(className="bi bi-person-circle fs-4"), href=PATH_USER, className="ms-3"),
        ], class_name=class_navitem)

    # return result
    class_brand = "fw-bold mx-0 text-primary fs-5"
    return dbc.Navbar(dbc.Container(children=[
        dbc.NavbarBrand(config_app_name, href=PATH_INTROS, class_name=class_brand),
        dbc.NavbarToggler(id="id-toggler"),
        dbc.Collapse(children=[
            dbc.Nav(nav_link_list, navbar=True, class_name="mx-auto"),
            dbc.Nav(nav_item_list, navbar=True, class_name=None),
        ], id="id-collapse", is_open=False, navbar=True),
    ], fluid=fluid), class_name="border-bottom py-2")


@app.callback(
    Output("id-collapse", "is_open"),
    Input("id-toggler", "n_clicks"),
    State("id-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
