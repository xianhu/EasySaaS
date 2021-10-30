# _*_ coding: utf-8 _*_

"""
page of alert
"""

from .common import layout_salert


def layout_404(pathname, search, return_href="/"):
    """
    layout of page
    """
    text_hd = "Page not found"
    text_sub = "This page is not found, click button to safe page."
    return layout_salert(text_hd, text_sub, "Back to safety", href=return_href)


def layout_expire(pathname, search, return_href="/"):
    """
    layout of page
    """
    text_hd = "Link expired"
    text_sub = "The link has already expired, click button to safe page."
    return layout_salert(text_hd, text_sub, "Back to safety", href=return_href)
