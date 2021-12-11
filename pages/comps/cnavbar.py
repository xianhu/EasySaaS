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
    class_navlink = "fw-bold text-white text-center border-bottom mx-md-1 px-md-4 py-md-3"
    class_intros = "bg-primary-down" if pathname == PATH_INTROS else "bg-primary-down-hover"
    class_analysis = "bg-primary-down" if pathname.startswith(PATH_ANALYSIS) else "bg-primary-down-hover"
    nav_link_list = [
        dbc.NavLink("Intros", href=PATH_INTROS, class_name=f"{class_navlink} {class_intros}"),
        dbc.NavLink("Analysis", href=PATH_ANALYSIS, class_name=f"{class_navlink} {class_analysis}"),
    ]

    # define components
    children_right = [
        html.A("Sign up", href=PATH_REGISTERE, className="text-white"),
        dbc.Button("Sign in", href=PATH_LOGIN, outline=True, color="light", class_name="fw-bold text-white ms-3"),
    ] if not flask_login.current_user.is_authenticated else [
        html.A(html.I(className="bi bi-bell fs-5 text-white"), href=PATH_USER, className=None),
        html.A(html.I(className="bi bi-person-circle fs-4 text-white"), href=PATH_USER, className="ms-3"),
    ]
    nav_item_list = dbc.NavItem(children_right, class_name="d-flex align-items-center mx-auto mx-md-0 my-1")

    # return result
    class_navbar = class_navbar or "bg-primary border-bottom py-0"
    return dbc.Navbar(dbc.Container(children=[
        dbc.NavbarBrand(children=[
            html.Img(src="assets/favicon0.png", style={"width": "1.5rem"}),
            html.Span(config_app_name, className="fs-5 fw-bold text-white align-middle ms-1"),
        ], href=PATH_INTROS),
        dbc.NavbarToggler(id="id-toggler", class_name="my-2"),
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
