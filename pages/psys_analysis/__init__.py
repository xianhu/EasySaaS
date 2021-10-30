# _*_ coding: utf-8 _*_

"""
page of sys-analysis
"""

from ..navbar import layout_navbar
from . import pdemo
from .consts import *


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_SYS_ANALYSIS or pathname == PATH_SYS_ANALYSIS_DEMO:
        content = pdemo.layout(pathname, search)

    # return result
    return [layout_navbar(pathname, search), content]
