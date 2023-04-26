# _*_ coding: utf-8 _*_

"""
alert page
"""

import feffery_antd_components as fac
from dash import html

from .paths import PATH_ROOT


def layout(pathname, search, status, text_title, text_subtitle, text_button, return_href):
    """
    layout of page
    """
    # define components
    kwargs_button = dict(type="primary", size="large", className="mt-2")
    button = fac.AntdButton(text_button, href=return_href, **kwargs_button)

    # define components
    sub_title = [fac.AntdText(text_subtitle), html.Br(), button]
    result_div = fac.AntdResult(status=status, title=text_title, subTitle=sub_title)

    # return result
    return html.Div(result_div, className="d-flex align-items-center justify-content-center vh-100")


def layout_403(pathname, search, return_href=PATH_ROOT):
    """
    layout of page
    """
    text_title = "No permission to access"
    text_subtitle = "You have no permission to access this page, click button to safe page."
    return layout(pathname, search, "403", text_title, text_subtitle, "Back to safety", return_href)


def layout_404(pathname, search, return_href=PATH_ROOT):
    """
    layout of page
    """
    text_title = "Page not found"
    text_subtitle = "This page is not found, click button to safe page."
    return layout(pathname, search, "404", text_title, text_subtitle, "Back to safety", return_href)


def layout_500(pathname, search, return_href=PATH_ROOT):
    """
    layout of page
    """
    text_title = "Server error"
    text_subtitle = "An error occurred on the server, click button to safe page."
    return layout(pathname, search, "500", text_title, text_subtitle, "Back to safety", return_href)


def layout_expired(pathname, search, return_href=PATH_ROOT):
    """
    layout of page
    """
    text_title = "Link expired"
    text_subtitle = "This link is expired, click button to safe page."
    return layout(pathname, search, "error", text_title, text_subtitle, "Back to safety", return_href)
