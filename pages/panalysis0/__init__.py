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
    class_link = "text-white mx-2 hover-success"
    navlink_list = [
        dbc.NavLink("Intros", id=f"id-{TAG}-intros", href="#", class_name=class_link),
        dbc.NavLink("Products", id=f"id-{TAG}-products", href="#", class_name=class_link),
        dbc.NavLink("Prices", id=f"id-{TAG}-prices", href="#", class_name=class_link),
        dbc.NavLink("Contacts", id=f"id-{TAG}-contacts", href="#", class_name=class_link),
    ]

    # define components
    navitem_right = dbc.NavItem(children=[
        dbc.Badge(5, id=f"id-{TAG}-badge", color="danger", href="#", class_name="text-decoration-none"),
        dbc.DropdownMenu(children=[
            dbc.DropdownMenuItem("Profile", id=f"id-{TAG}-profile", href="#"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Logout", href=PATH_LOGIN),
        ], align_end=True, label=user.email.split("@")[0], class_name="ms-1"),
    ], class_name="d-flex align-items-center justify-content-center")

    # define components
    navbar = dbc.Navbar(dbc.Container(children=[
        cbrand.layout(class_text=None, class_name=None),
        dbc.Nav(navlink_list, navbar=True, class_name="mx-auto"),
        dbc.Nav(navitem_right, navbar=True, class_name=None),
    ], fluid=False), color="primary", class_name="sticky-top py-1")

    # define components
    content = dbc.Container(id=f"id-{TAG}-content", fluid=False, class_name="py-2 mb-auto")
    footer = cfooter.layout(fluid=False, class_name="sticky-bottom py-2 border-top")

    # return result
    return html.Div([navbar, content, footer], className="bg-light vh-100 overflow-auto d-flex flex-column")
