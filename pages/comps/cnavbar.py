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


def layout(pathname, search, fluid=None, class_container=None, class_navbar=None):
    """
    layout of components
    """
    # define components
    class_navlink = "fw-bold text-white border-bottom mx-auto mx-md-4"
    nav_link_list = [
        dbc.NavLink("Intros", href=PATH_INTROS, class_name=class_navlink),
        dbc.NavLink("Analysis", href=PATH_ANALYSIS, class_name=class_navlink),
    ]

    # define components
    if not flask_login.current_user.is_authenticated:
        class_button = "fw-bold text-white ms-3"
        nav_item_list = dbc.NavItem([
            html.A("Sign up", href=PATH_REGISTERE, className="text-white"),
            dbc.Button("Sign in", href=PATH_LOGIN, outline=True, color="light", class_name=class_button),
        ], class_name="d-flex align-items-center mx-auto mx-md-0 mt-2 mt-md-0")
    else:
        nav_item_list = dbc.NavItem([
            html.A(html.I(className="bi bi-bell fs-5 text-white"), href=PATH_USER),
            html.A(html.I(className="bi bi-person-circle fs-4 text-white"), href=PATH_USER, className="ms-3"),
        ], class_name="d-flex align-items-center mx-auto mx-md-0 mt-2 mt-md-0")

    # return result
    class_brand = "fs-5 fw-bold text-white mx-0"
    class_navbar = class_navbar or "bg-primary border-bottom py-2"
    return dbc.Navbar(dbc.Container(children=[
        dbc.NavbarBrand(config_app_name, href=PATH_INTROS, class_name=class_brand),
        dbc.NavbarToggler(id="id-toggler"),
        dbc.Collapse(children=[
            dbc.Nav(nav_link_list, navbar=True, class_name="mx-auto"),
            dbc.Nav(nav_item_list, navbar=True, class_name=None),
        ], id="id-collapse", is_open=False, navbar=True),
    ], fluid=fluid, class_name=class_container), class_name=class_navbar)


@app.callback(
    Output("id-collapse", "is_open"),
    Input("id-toggler", "n_clicks"),
    State("id-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
