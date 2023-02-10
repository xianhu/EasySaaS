# _*_ coding: utf-8 _*_

"""
compontents of header
"""

import dash
import feffery_antd_components as fac
from dash import html

from config import config_app_name
from utility.paths import PATH_USER, PATH_LOGIN


def get_component_header_brand(logo="favicon1.svg"):
    """
    layout of component
    """
    src_logo = dash.get_asset_url(logo)
    kwargs_logo = dict(width="30px", height="30px", preview=False)
    return fac.AntdRow(children=[
        fac.AntdCol(fac.AntdImage(src=src_logo, **kwargs_logo)),
        fac.AntdCol(html.Span(config_app_name, className="fs-4 ms-1")),
    ], align="middle", justify="start", className=None)


def get_component_header_user(user_title, dot=True):
    """
    layout of component
    """
    return fac.AntdBadge(fac.AntdDropdown(menuItems=[
        {"title": "Profile", "href": f"{PATH_USER}?tab=profile"},
        {"title": "Settings", "href": f"{PATH_USER}?tab=settings"},
        {"isDivider": True},
        {"title": "Logout", "href": PATH_LOGIN},
    ], title=user_title, buttonMode=True), dot=dot)


def get_component_header(title, user_title, dot=True):
    """
    layout of component
    """
    # define components
    col_title = fac.AntdCol(title or get_component_header_brand())
    col_dropdown = fac.AntdCol(get_component_header_user(user_title, dot=dot))

    # return result
    class_row = "bg-white border-bottom sticky-top px-4 py-2"
    kwargs_row = dict(align="middle", justify="space-between")
    return fac.AntdRow([col_title, col_dropdown], **kwargs_row, className=class_row)
