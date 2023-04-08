# _*_ coding: utf-8 _*_

"""
components of header
"""

import feffery_antd_components as fac

from utility.paths import *


def get_component_header_user(user_title, dot=False):
    """
    layout of component
    """
    return fac.AntdBadge(fac.AntdDropdown(menuItems=[
        {"title": "Settings", "href": PATH_USER},
        {"isDivider": True},
        {"title": "Projects", "href": PATH_PROJECTS},
        {"isDivider": True},
        {"title": "Logout", "href": PATH_LOGIN},
    ], title=user_title, buttonMode=True), dot=dot)


def get_component_header(children_left, children_right, children_middle=None):
    """
    layout of component
    """
    class_row = "bg-white border-bottom sticky-top px-4 py-2"
    return fac.AntdRow(children=[
        fac.AntdCol(children_left, className=None),
        fac.AntdCol(children_middle, className=None),
        fac.AntdCol(children_right, className=None),
    ], align="middle", justify="space-between", className=class_row)
