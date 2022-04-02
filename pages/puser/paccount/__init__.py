# _*_ coding: utf-8 _*_

"""
account page
"""

from dash import html

from . import cbasic, cnofity, cpwd


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        cbasic.layout(pathname, search, class_name=None),
        cpwd.layout(pathname, search, class_name="mt-4"),
        cnofity.layout(pathname, search, class_name="mt-4"),
    ], className="mb-4")
