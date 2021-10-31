# _*_ coding: utf-8 _*_

"""
page of analysis
"""

from ..navbar import layout_navbar
from ..paths import *
from . import pdemo


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_ANALYSIS or pathname == PATH_ANALYSIS_DEMO:
        content = pdemo.layout(pathname, search)

    # return result
    return [layout_navbar(pathname, search), content]
