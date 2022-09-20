# _*_ coding: utf-8 _*_

"""
intros page
"""

import dash_bootstrap_components as dbc
from dash import html

from components import cfooter, cnavbar
from utility.paths import NAV_LINKS


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    nav_links = []
    for title, _id, href, class_name in NAV_LINKS:
        if href == pathname:
            class_name = "border-bottom border-primary"
        nav_links.append([title, _id, href, class_name])

    # return result
    return html.Div(children=[
        cnavbar.layout(nav_links, fluid=False, class_name=None),
        dbc.Container("intros page", fluid=False, class_name="my-3"),
        cfooter.layout(fluid=False, class_name=None),
    ], className="d-flex flex-column vh-100")
