# _*_ coding: utf-8 _*_

"""
intros page
"""

from dash import html
import dash_bootstrap_components as dbc

from ..components import cfooter, cnavbar
from . import cintros, cplans, ccontact, cheader


def layout(pathname, search):
    """
    layout of page
    """
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=None),
        dbc.Container(children=[
            cheader.layout(pathname, search, class_name=None),
            cintros.layout(pathname, search, class_name="mt-5"),
            cplans.layout(pathname, search, class_name="mt-5"),
            ccontact.layout(pathname, search, class_name="mt-5"),
        ], fluid=None, class_name="my-5"),
        cfooter.layout(pathname, search, fluid=None),
    ], className="d-flex flex-column vh-100")
