# _*_ coding: utf-8 _*_

"""
billing page
"""

from dash import html

from . import cinvoice, cplan


def layout(pathname, search):
    """
    layout of page
    """
    return html.Div(children=[
        cplan.layout(pathname, search, class_name=None),
        cinvoice.layout(pathname, search, class_name="mt-4"),
    ], className="mb-4")
