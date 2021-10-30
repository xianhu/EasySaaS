# _*_ coding: utf-8 _*_

"""
navbar of page
"""

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app
from config import config_app_name

from .pasign.consts import *
from .pindex.consts import *
from .pmine.consts import *
from .psys_analysis.consts import *


def layout_navbar(pathname, search):
    """
    layout of navbar
    """
    # define class
    class_brand = "fw-bold mx-0 text-primary fs-5"
    class_icon = "fw-bold mx-0 text-secondary fs-5 hover-primary"
    class_navlink = "fw-bold mx-auto mx-md-4 mx-lg-4 hover-primary"
    class_navitem = "fw-bold mx-auto mx-md-0 mx-lg-0 d-flex align-items-center"

    # define components
    if not flask_login.current_user.is_authenticated:
        args_button = {"outline": True, "color": "primary", "class_name": "fw-bold"}
        nav_item_children = dbc.NavItem([
            html.A("Sign up", href=PATH_REGISTER_EMAIL, className="me-3"),
            dbc.Button("Sign in", href=PATH_LOGIN, **args_button),
        ], class_name=class_navitem)
    else:
        user_name = flask_login.current_user.email
        nav_item_children = dbc.NavItem([
            html.A(html.I(className="bi bi-bell " + class_icon), href=PATH_NOTIFY, className="me-3"),
            html.A(html.I(className="bi bi-arrow-up-circle " + class_icon), href=PATH_UPGRADE, className="me-3"),
            html.A(html.I(className="bi bi-person-circle fs-4"), href=PATH_PROFILE, title=user_name),
        ], class_name=class_navitem)

    # return result
    href_brand = PATH_INDEX if pathname in PATH_SET_INDEX else PATH_SYS_ANALYSIS
    return dbc.Navbar(dbc.Container(children=[
        dbc.NavbarBrand(config_app_name, href=href_brand, class_name=class_brand),
        dbc.NavbarToggler(id="id-toggler"),
        dbc.Collapse(children=[
            dbc.Nav(children=[
                dbc.NavLink("Intros", href=PATH_INTROS, class_name=class_navlink),
                dbc.NavLink("Pricing", href=PATH_PRICING, class_name=class_navlink),
                dbc.NavLink("About", href=PATH_ABOUT, class_name=class_navlink),
                dbc.NavLink("Analysis", href=PATH_SYS_ANALYSIS, class_name=class_navlink),
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
