# _*_ coding: utf-8 _*_

"""
page of analysis
"""

from dash import html

from ..common import CLASS_DIV_CONTENT
from ..navbar import layout_navbar
from ..paths import *
from . import pdemo


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    top_navbar = layout_navbar(pathname, search)

    # content
    content = None
    if pathname == PATH_ANALYSIS or pathname == PATH_ANALYSIS_DEMO:
        content = pdemo.layout(pathname, search)

    # return result
    return [top_navbar, html.Div([content, ], className=CLASS_DIV_CONTENT)]
