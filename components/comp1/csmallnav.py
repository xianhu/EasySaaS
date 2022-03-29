# _*_ coding: utf-8 _*_

"""
small navbar component
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search, id_tg, title, fluid=None, class_name=None):
    """
    layout of component
    """
    # define components
    icon = html.A(html.I(className="bi bi-list fs-1"))
    toggler = dbc.NavbarToggler(icon, id=id_tg, class_name="border")

    # define components
    small_nav = dbc.Row(children=[
        dbc.Col(title, width="auto", class_name="text-primary"),
        dbc.Col(toggler, width="auto", class_name="my-2"),
    ], align="center", justify="between", class_name=None)

    # return result
    class_name = class_name or "d-md-none border-bottom"
    return dbc.Container(small_nav, fluid=fluid, class_name=class_name)
