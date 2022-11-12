# _*_ coding: utf-8 _*_

"""
alert page
"""

import feffery_antd_components as fac
from dash import html

from utility.paths import PATH_ROOT


def layout(pathname, search, status, text_title, text_subtitle, text_button, return_href):
    """
    layout of page
    """
    kwargs = dict(type="primary", size="large", className="mt-2")
    return fac.AntdResult(
        status=status,
        title=text_title,
        subTitle=[
            fac.AntdText(text_subtitle), html.Br(),
            fac.AntdButton(text_button, href=return_href, **kwargs),
        ]
    )


def layout_404(pathname, search, return_href=PATH_ROOT):
    """
    layout of page
    """
    text_title = "Page not found"
    text_subtitle = "This page is not found, click button to safe page."
    return layout(pathname, search, "404", text_title, text_subtitle, "Back to safety", return_href)


def layout_expired(pathname, search, return_href=PATH_ROOT):
    """
    layout of page
    """
    text_title = "Link expired"
    text_subtitle = "The link has expired, click button to safe page."
    return layout(pathname, search, "error", text_title, text_subtitle, "Back to safety", return_href)
