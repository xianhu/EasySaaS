# _*_ coding: utf-8 _*_

"""
user page
"""

import feffery_antd_components as fac
import flask_login
from dash import html

from ..comps import header as comps_header

TAG = "user"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

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
        ], defaultActiveKey="settings", tabPosition="left", className="w-75 m-auto mt-4"),
    ], className="bg-main vh-100 overflow-auto")
