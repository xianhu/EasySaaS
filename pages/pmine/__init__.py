# _*_ coding: utf-8 _*_

"""
page of mine
"""

from dash import html

from ..common import CLASS_DIV_CONTENT
from ..navbar import layout_navbar
from ..paths import *
from . import pnotify, pprofile, pupgrade
from .catalog import layout_catalog


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    top_navbar = layout_navbar(pathname, search)
    left_catalog = layout_catalog(pathname, search)

    # content
    content = None
    if pathname == PATH_MINE or pathname == PATH_MINE_PROFILE:
        content = pprofile.layout(pathname, search)
    elif pathname == PATH_MINE_NOTIFY:
        content = pnotify.layout(pathname, search)
    elif pathname == PATH_MINE_UPGRADE:
        content = pupgrade.layout(pathname, search)

    # return result
    return [top_navbar, html.Div([left_catalog, content], className=CLASS_DIV_CONTENT)]
