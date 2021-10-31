# _*_ coding: utf-8 _*_

"""
page of analysis
"""

import dash_bootstrap_components as dbc

from ..common import CLASS_CONTAINER_CONTENT
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
    return [top_navbar, dbc.Container([content, ], class_name=CLASS_CONTAINER_CONTENT)]
