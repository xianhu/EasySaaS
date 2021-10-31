# _*_ coding: utf-8 _*_

"""
page of index
"""

import dash_bootstrap_components as dbc

from ..common import CLASS_CONTAINER_CONTENT
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
    if pathname == PATH_INDEX or pathname == PATH_INTROS:
        content = pintros.layout(pathname, search)
    elif pathname == PATH_PRICING:
        content = ppricing.layout(pathname, search)
    elif pathname == PATH_ABOUT:
        content = pabout.layout(pathname, search)

    # return result
    return [top_navbar, dbc.Container([content, ], class_name=CLASS_CONTAINER_CONTENT)]
