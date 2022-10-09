# _*_ coding: utf-8 _*_

"""
navbar component
"""

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, html

from utility.paths import *
from . import cbrand


def layout(nav_links, curr_path, fluid=None, class_name=None):
    """
    layout of component
    """
    # define components
    nav_children = []
    for title, _id, href in nav_links:
        class_link = "border-bottom border-white" if href == curr_path else ""
        class_link = f"fw-bold text-white text-center mx-md-1 p-md-2 {class_link}"
        nav_children.append(dbc.NavLink(title, id=_id, href=href, class_name=class_link))
    nav_middle = dbc.Nav(nav_children, navbar=True, class_name="mx-auto")

    # define components
    nav_right = dbc.Nav(dbc.NavItem(children=[
        html.A("Sign up", href=PATH_REGISTER, className="me-3"),
        dbc.Button("Sign in", href=PATH_LOGIN, color="success", outline=True),
    ] if not flask_login.current_user.is_authenticated else [
        html.A(html.I(className="bi bi-bell fs-5"), href=f"{PATH_USER}#template"),
        html.A(html.I(className="bi bi-person-circle fs-4"), href=PATH_USER, className="ms-3"),
    ], class_name="d-flex align-items-center justify-content-center py-1 py-md-0"), navbar=True)

    # return result
    return dbc.Navbar(dbc.Container(children=[
        cbrand.layout(href=PATH_ROOT, class_name=None),
        dbc.NavbarToggler(id="id-toggler", class_name="border-white"),
        dbc.Collapse([nav_middle, nav_right], id="id-collapse", navbar=True),
    ], fluid=fluid), dark=True, color="primary", class_name=f"py-1 {class_name}")


@dash.callback(
    Output("id-collapse", "is_open"),
    Input("id-toggler", "n_clicks"),
    State("id-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
