# _*_ coding: utf-8 _*_

"""
small navbar component
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(id_tg, title, fluid=None, class_name=None):
    """
    layout of component
    """
    # define components
    class_tg = "border border-dark rounded px-2"
    icon_tg = html.A(html.I(className="bi bi-list fs-1"))
    toggler = dbc.NavbarToggler(icon_tg, id=id_tg, class_name=class_tg)

    # define components
    row = dbc.Row(children=[
        dbc.Col(title, width="auto", class_name=None),
        dbc.Col(toggler, width="auto", class_name=None),
    ], align="center", justify="between", class_name=None)

    # return result
    class_name = class_name or "d-md-none border-bottom py-1"
    return dbc.Container(row, fluid=fluid, class_name=class_name)
