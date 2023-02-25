# _*_ coding: utf-8 _*_

"""
compontents of header
"""

import dash
import feffery_antd_components as fac
from dash import html

from config import config_app_name
from utility.paths import *


def get_component_header_brand(path_logo="favicon1.svg"):
    """
    layout of component
    """
    # define components
    src_logo = dash.get_asset_url(path_logo)
    kwargs_logo = dict(width="30px", height="30px", preview=False)

    # define components
    col_logo = fac.AntdCol(fac.AntdImage(src=src_logo, **kwargs_logo))
    col_text = fac.AntdCol(html.Span(config_app_name, className="fs-4 ms-1"))
    row_brand = fac.AntdRow([col_logo, col_text], align="middle", justify="start")

    # return result
    return html.A(row_brand, href=PATH_ROOT, className="text-dark text-decoration-none")


def get_component_header_user(user_title, dot=True):
    """
    layout of component
    """
    return fac.AntdBadge(fac.AntdDropdown(menuItems=[
        {"title": "Profile", "href": f"{PATH_USER}?tab=profile"},
        {"title": "Settings", "href": f"{PATH_USER}?tab=settings"},
        {"isDivider": True},
        {"title": "Projects", "href": PATH_PROJECTS},
        {"isDivider": True},
        {"title": "Logout", "href": PATH_LOGIN},
    ], title=user_title, buttonMode=True), dot=dot, className=None)


def get_component_header(
        chilren_left=None, path_logo="favicon1.svg",
        children_right=None, user_title=None, dot=True,
        children_middle=None, class_row=None,
):
    """
    layout of component
    """
    # define components
    if chilren_left:
        col_left = fac.AntdCol(chilren_left)
    else:
        col_left = fac.AntdCol(get_component_header_brand(path_logo=path_logo))

    # define components
    if children_right:
        col_right = fac.AntdCol(children_right)
    else:
        col_right = fac.AntdCol(get_component_header_user(user_title, dot=dot))

    # define components
    col_middle = fac.AntdCol(children_middle)

    # return result
    kwargs_row = dict(align="middle", justify="space-between")
    class_row = class_row or "bg-white border-bottom sticky-top px-4 py-2"
    return fac.AntdRow([col_left, col_middle, col_right], **kwargs_row, className=class_row)
