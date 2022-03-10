# _*_ coding: utf-8 _*_

"""
small navbar component
"""

from dash import html
import dash_bootstrap_components as dbc


def layout(pathname, search, toggler_id, title, class_title=None, fluid=None, class_container=None):
    """
    layout of component
    """
    # define components
    icon = html.A(html.I(className="bi bi-list fs-1"))
    toggler = dbc.NavbarToggler(icon, id=toggler_id, class_name="border")

    # define components
    class_title = class_title or "text-primary"
    small_nav = dbc.Row(children=[
        dbc.Col(title, width="auto", class_name=class_title),
        dbc.Col(toggler, width="auto", class_name="my-2"),
    ], align="center", justify="between", class_name=None)

    # return result
    class_container = class_container or "d-md-none border-bottom"
    return dbc.Container(small_nav, fluid=fluid, class_name=class_container)
