# _*_ coding: utf-8 _*_

"""
page of mine
"""

from ..navbar import layout_navbar
from ..paths import *
from . import pnotify, pprofile, pupgrade


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_MINE or pathname == PATH_MINE_PROFILE:
        content = pprofile.layout(pathname, search)
    elif pathname == PATH_MINE_NOTIFY:
        content = pnotify.layout(pathname, search)
    elif pathname == PATH_MINE_UPGRADE:
        content = pupgrade.layout(pathname, search)

    # return result
    return [layout_navbar(pathname, search), content]
