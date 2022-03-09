# _*_ coding: utf-8 _*_

"""
small navbar component
"""

from dash import html
import dash_bootstrap_components as dbc


def layout(pathname, search, toggler_id, title, title_class=None):
    """
    layout of component
    """
    # define components
    icon = html.A(html.I(className="bi bi-list fs-1"))
    toggler = dbc.NavbarToggler(icon, id=toggler_id, class_name="border")

    # return result
    class_title = title_class or "text-primary"
    return dbc.Row(children=[
        dbc.Col(title, width="auto", class_name=class_title),
        dbc.Col(toggler, width="auto", class_name="my-2"),
    ], align="center", justify="between", class_name="d-md-none border-bottom w-100 mx-auto")
