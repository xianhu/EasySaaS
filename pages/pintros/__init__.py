# _*_ coding: utf-8 _*_

"""
intros page
"""

from dash import html
import dash_bootstrap_components as dbc

from ..components import cfooter, cnavbar
from .components import ccontact, cheader, cintros, cplans


def layout(pathname, search):
    """
    layout of page
    """
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=None),
        dbc.Container(children=[
            cheader.layout(pathname, search),
            cintros.layout(pathname, search),
            cplans.layout(pathname, search),
            ccontact.layout(pathname, search),
        ], fluid=None, class_name="mb-5"),
        cfooter.layout(pathname, search, fluid=None),
    ])
