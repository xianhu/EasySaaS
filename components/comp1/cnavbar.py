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


def layout(nav_links, fluid=None, class_name=None):
    """
    layout of component
    """
    # define components
    nav_children = []
    class_link = "fw-bold text-center mx-md-1 p-md-3"
    for title, _id, href, _class in nav_links:
        kwargs_link = dict(id=_id, href=href, class_name=f"{class_link} {_class}")
        nav_children.append(dbc.NavLink(title, **kwargs_link))
    nav = dbc.Nav(nav_children, navbar=True, class_name="mx-auto")

    # define components
    kwargs_button = dict(color="primary", outline=True)
    nav_right = dbc.Nav(dbc.NavItem(children=[
        html.A("Sign up", href=PATH_REGISTERE, className=None),
        dbc.Button("Sign in", href=PATH_LOGIN, **kwargs_button, class_name="fw-bold ms-3"),
    ] if not flask_login.current_user.is_authenticated else [
        html.A(html.I(className="bi bi-bell fs-5"), href=f"{PATH_USER}#template"),
        html.A(html.I(className="bi bi-person-circle fs-4"), href=PATH_USER, className="ms-3"),
    ], class_name="d-flex align-items-center justify-content-center py-1 py-md-0"), navbar=True)

    # return result
    class_name = class_name or "border-bottom py-0"
    return dbc.Navbar(dbc.Container(children=[
        cbrand.layout(href=PATH_ROOT, class_name=None),
        dbc.NavbarToggler(id="id-toggler", class_name="my-2"),
        dbc.Collapse([nav, nav_right], id="id-collapse", navbar=True),
    ], fluid=fluid, class_name=None), class_name=class_name)


@dash.callback(
    Output("id-collapse", "is_open"),
    Input("id-toggler", "n_clicks"),
    State("id-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
