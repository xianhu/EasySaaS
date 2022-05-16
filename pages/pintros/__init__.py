# _*_ coding: utf-8 _*_

"""
intros page
"""

import dash_bootstrap_components as dbc
from dash import html

from utility.paths import NAV_LINKS
from components import cfooter, cnavbar
from . import ccontact, cheader, cintros, cplans


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    nav_links = []
    for title, _id, href, _class in NAV_LINKS:
        if href == pathname:
            _class = "border-bottom border-primary"
        nav_links.append([title, _id, href, _class])

    # return result
    return html.Div(children=[
        cnavbar.layout(nav_links, fluid=False, class_name=None),
        dbc.Container(children=[
            cheader.layout(class_name=None),
            cintros.layout(class_name="mt-5"),
            cplans.layout(class_name="mt-5"),
            ccontact.layout(class_name="mt-5"),
        ], fluid=False, class_name="my-5"),
        cfooter.layout(fluid=False, class_name=None),
    ], className="d-flex flex-column vh-100")
