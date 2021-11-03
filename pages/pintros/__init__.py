# _*_ coding: utf-8 _*_

"""
page of intros
"""

from dash import html

from ..comps import cnavbar, cfooter, cpricing
from ..paths import *
from . import lheader


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    navbar = cnavbar.layout(pathname, search)
    footer = cfooter.layout(pathname, search)

    # define page layout
    content = html.Div(children=[
        lheader.layout(pathname, search),
        cpricing.layout(pathname, search),
    ], className="")

    # return result
    return [navbar, content, footer]
