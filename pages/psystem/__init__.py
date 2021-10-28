# _*_ coding: utf-8 _*_

"""
page of system
"""

from ..consts import *
from ..navbar import layout_navbar
from . import panalysis


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_SYSTEM or pathname == PATH_ANALYSIS:
        content = panalysis.layout(pathname, search)

    # return result
    return [layout_navbar(pathname, search), content]
