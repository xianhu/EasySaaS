# _*_ coding: utf-8 _*_

"""
planpay page
"""

from dash import html

from . import cinvoice, cplan


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        cplan.layout(class_name=None),
        cinvoice.layout(class_name="mt-4"),
    ], className="mb-4")
