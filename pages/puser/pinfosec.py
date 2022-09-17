# _*_ coding: utf-8 _*_

"""
infosec page
"""

from dash import html

from . import cpwd, cbasic


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        cbasic.layout(class_name=None),
        cpwd.layout(class_name="mt-4"),
    ], className="mb-4")
