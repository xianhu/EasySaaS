# _*_ coding: utf-8 _*_

"""
page of mine
"""

from ..consts import *
from ..navbar import layout_navbar
from . import pnotify, pprofile, pupgrade


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_NOTIFY:
        content = pnotify.layout(pathname, search)
    elif pathname == PATH_UPGRADE:
        content = pupgrade.layout(pathname, search)
    elif pathname == PATH_PROFILE:
        content = pprofile.layout(pathname, search)

    # return result
    return [layout_navbar(pathname, search), content]
