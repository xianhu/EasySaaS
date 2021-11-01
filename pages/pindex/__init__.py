# _*_ coding: utf-8 _*_

"""
page of index
"""

from dash import html

from ..common import CLASS_DIV_CONTENT
from ..navbar import layout_navbar
from ..paths import *
from . import pabout, pintros, ppricing


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    top_navbar = layout_navbar(pathname, search)

    # content
    content = None
    if pathname == PATH_INTROS:
        content = pintros.layout(pathname, search)
    elif pathname == PATH_PRICING:
        content = ppricing.layout(pathname, search)
    elif pathname == PATH_ABOUT:
        content = pabout.layout(pathname, search)

    # return result
    return [top_navbar, html.Div([content, ], className=CLASS_DIV_CONTENT)]
