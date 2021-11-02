# _*_ coding: utf-8 _*_

"""
navbar of page
"""

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app
from config import config_app_name

from .paths import *


def layout_navbar(pathname, search):
    """
    layout of navbar
    """
    # define class
    class_brand = "fw-bold mx-0 text-primary fs-5"
    class_icon = "fw-bold mx-0 text-secondary fs-5 hover-primary"
    class_navlink = "fw-bold mx-auto mx-md-4 hover-primary"
    class_navitem = "fw-bold mx-auto mx-md-0 d-flex align-items-center"

    # define components
    if not flask_login.current_user.is_authenticated:
        args_button = {"outline": True, "color": "primary"}
        nav_item_children = dbc.NavItem([
            html.A("Sign up", href=PATH_EMAIL_REGISTER, className=None),
            dbc.Button("Sign in", href=PATH_LOGIN, **args_button, className="fw-bold ms-3"),
        ], class_name=class_navitem)
    else:
        user_name = flask_login.current_user.email
        nav_item_children = dbc.NavItem([
            html.A(html.I(className="bi bi-bell " + class_icon), href=PATH_MINE_NOTIFY, className=None),
            html.A(html.I(className="bi bi-arrow-up-circle " + class_icon), href=PATH_MINE_UPGRADE, className="ms-3"),
            html.A(html.I(className="bi bi-person-circle fs-4"), href=PATH_MINE_PROFILE, title=user_name, className="ms-3"),
        ], class_name=class_navitem)

    # return result
    return dbc.Navbar(dbc.Container(children=[
        dbc.NavbarBrand(config_app_name, href=PATH_INTROS, class_name=class_brand),
        dbc.NavbarToggler(id="id-toggler"),
        dbc.Collapse(children=[
            dbc.Nav(children=[
                dbc.NavLink("Intros", href=PATH_INTROS, class_name=class_navlink),
                dbc.NavLink("Analysis", href=PATH_ANALYSIS, class_name=class_navlink),
            ], navbar=True, class_name="mx-auto"),
            dbc.Nav(nav_item_children, navbar=True, class_name=None),
        ], id="id-collapse", is_open=False, navbar=True),
    ]), class_name="border-bottom px-3 py-2")


@app.callback(
    Output("id-collapse", "is_open"),
    Input("id-toggler", "n_clicks"),
    State("id-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
