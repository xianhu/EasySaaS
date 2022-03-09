# _*_ coding: utf-8 _*_

"""
intros page
"""

from dash import html
import dash_bootstrap_components as dbc

from ..components import cfooter, cnavbar
from . import pheader, pintros, pplans, pcontact


def layout(pathname, search):
    """
    layout of page
    """
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=None),
        dbc.Container(children=[
            pheader.layout(pathname, search),
            pintros.layout(pathname, search),
            pplans.layout(pathname, search),
            pcontact.layout(pathname, search),
        ], fluid=None, class_name="mb-5"),
        cfooter.layout(pathname, search, fluid=None),
    ])
