# _*_ coding: utf-8 _*_

"""
page of alert
"""

from ..consts import PATH_INDEX
from .comps import layout_salert


def layout_404(pathname, search):
    """
    layout of page
    """
    text_hd = "Page not found"
    text_sub = "This page is not found, click button to safe page."
    return layout_salert(text_hd, text_sub, "Back to safety", href=PATH_INDEX)


def layout_expire(pathname, search):
    """
    layout of page
    """
    text_hd = "Link expired"
    text_sub = "The link has already expired, click button to safe page."
    return layout_salert(text_hd, text_sub, "Back to safety", href=PATH_INDEX)
