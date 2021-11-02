# _*_ coding: utf-8 _*_

"""
page of intros
"""

from dash import html

from ..common import CLASS_DIV_CONTENT
from ..navbar import layout_navbar
from ..paths import *
from . import labout, lheader, lpricing


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    top_navbar = layout_navbar(pathname, search)

    # define page layout
    content = html.Div(children=[
        lheader.layout(pathname, search),
        lpricing.layout(pathname, search),
        labout.layout(pathname, search),
    ], className="")

    # return result
    return [top_navbar, content]
