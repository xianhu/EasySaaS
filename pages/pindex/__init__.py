# _*_ coding: utf-8 _*_

"""
page of index
"""

from ..consts import *
from ..footer import layout_footer
from ..navbar import layout_navbar
from . import pabout, pintros, ppricing


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_INDEX or pathname == PATH_INTROS:
        content = pintros.layout(pathname, search)

    if pathname == PATH_PRICING:
        content = ppricing.layout(pathname, search)

    if pathname == PATH_ABOUT:
        content = pabout.layout(pathname, search)

    # return result
    return [layout_navbar(pathname, search), content, layout_footer(pathname, search)]
