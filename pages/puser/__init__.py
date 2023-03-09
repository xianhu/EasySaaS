# _*_ coding: utf-8 _*_

"""
user page
"""

import logging
import urllib.parse

import feffery_antd_components as fac
import flask_login
from dash import html

from .. import palert
from ..comps import header as comps_header

TAG = "user"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # check tab's name
    try:
        search = urllib.parse.parse_qs(search.lstrip("?").strip())
        assert search["tab"][0] in ("profile", "settings")
    except Exception as excep:
        logging.error("get tab failed: %s", excep)
        return palert.layout_500(pathname, search)
    tab = search["tab"][0]

    # define components
    style = {"minHeight": "300px"}
    div_profile = html.Div("Profile", className="bg-white p-3", style=style)
    div_settings = html.Div("Settings", className="bg-white p-3", style=style)

    # return result
    return html.Div(children=[
        comps_header.get_component_header(user_title=user_title, dot=True),
        fac.AntdTabs(children=[
            fac.AntdTabPane(div_profile, key="profile", tab="Profile"),
            fac.AntdTabPane(div_settings, key="settings", tab="Settings"),
        ], defaultActiveKey=tab, tabPosition="left", className="w-75 m-auto mt-4"),
    ], className="bg-main vh-100 overflow-auto")
