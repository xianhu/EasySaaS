# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
import flask_login
from dash import html

from components import cbrand, cfooter
from utility.paths import PATH_LOGIN

TAG = "analysis0"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    user = flask_login.current_user

    # define components
    class_link = "fw-bold text-white text-center mx-2"
    navlink_list = [
        dbc.NavLink("Intros", id=f"id-{TAG}-intros", href="#", class_name=class_link),
        dbc.NavLink("Products", id=f"id-{TAG}-products", href="#", class_name=class_link),
        dbc.NavLink("Prices", id=f"id-{TAG}-prices", href="#", class_name=class_link),
        dbc.NavLink("Contacts", id=f"id-{TAG}-contacts", href="#", class_name=class_link),
    ]

    # define components
    navitem_bottom = dbc.NavItem(children=[
        dbc.Badge(5, color="danger", href="#", class_name="text-decoration-none"),
        dbc.DropdownMenu(children=[
            dbc.DropdownMenuItem("Basic Profile", href="#"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Logout", href=PATH_LOGIN)
        ], label=user.email.split("@")[0], class_name="ms-1"),
    ], class_name="d-flex align-items-center")

    navbar = dbc.Navbar(dbc.Container(children=[
        cbrand.layout(),
        dbc.Nav(navlink_list, navbar=True, class_name="mx-auto"),
        dbc.Nav(navitem_bottom, navbar=True, class_name=None),
    ], fluid=False), color="primary", class_name="py-1")

    # define components
    content = dbc.Container("analysis page", fluid=False, class_name="my-2")
    footer = cfooter.layout(fluid=False, class_name=None)

    # return result
    return html.Div([navbar, content, footer], className="d-flex flex-column vh-100")
