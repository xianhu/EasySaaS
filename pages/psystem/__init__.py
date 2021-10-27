# _*_ coding: utf-8 _*_

"""
page of system
"""

from ..consts import *
from ..footer import layout_footer
from ..navbar import layout_navbar
from . import panalysis, pnotify, pprofile, pupgrade


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_SYSTEM or pathname == PATH_ANALYSIS:
        content = panalysis.layout(pathname, search)

    if pathname == PATH_NOTIFY:
        content = pnotify.layout(pathname, search)

    if pathname == PATH_UPGRADE:
        content = pupgrade.layout(pathname, search)

    if pathname == PATH_PROFILE:
        content = pprofile.layout(pathname, search)

    # return result
    return [layout_navbar(pathname, search), content, layout_footer(pathname, search)]
