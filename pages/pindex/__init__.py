# _*_ coding: utf-8 _*_

"""
page of index
"""

from ..navbar import layout_navbar
from . import pabout, pintros, ppricing
from .consts import *


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_INDEX or pathname == PATH_INTROS:
        content = pintros.layout(pathname, search)
    elif pathname == PATH_PRICING:
        content = ppricing.layout(pathname, search)
    elif pathname == PATH_ABOUT:
        content = pabout.layout(pathname, search)

    # return result
    return [layout_navbar(pathname, search), content]
