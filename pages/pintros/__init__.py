# _*_ coding: utf-8 _*_

"""
intros page
"""

import dash_bootstrap_components as dbc
from dash import html

from components import cfooter, cnavbar
from . import ccontact, cheader, cintros, cplans


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        cnavbar.layout(fluid=False, class_name=None),
        dbc.Container(children=[
            cheader.layout(pathname, search, class_name=None),
            cintros.layout(pathname, search, class_name="mt-5"),
            cplans.layout(pathname, search, class_name="mt-5"),
            ccontact.layout(pathname, search, class_name="mt-5"),
        ], fluid=False, class_name="my-5"),
        cfooter.layout(fluid=False, class_name=None),
    ], className="d-flex flex-column vh-100")
