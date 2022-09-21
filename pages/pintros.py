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
    # return result
    return html.Div(children=[
        cnavbar.layout(NAV_LINKS, curr_path=pathname, fluid=False, class_name=None),
        dbc.Container("intros page", fluid=False, class_name="my-3"),
        cfooter.layout(fluid=False, class_name=None),
    ], className="d-flex flex-column vh-100")
