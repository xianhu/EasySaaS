# _*_ coding: utf-8 _*_

"""
page of intros
"""

from dash import html

from ..navbar import layout_navbar
from ..footer import layout_footer
from ..paths import *
from . import lheader, lpricing


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    navbar = layout_navbar(pathname, search)
    footer = layout_footer(pathname, search)

    # define page layout
    content = html.Div(children=[
        lheader.layout(pathname, search),
        lpricing.layout(pathname, search),
    ], className="")

    # return result
    return [navbar, content, footer]
