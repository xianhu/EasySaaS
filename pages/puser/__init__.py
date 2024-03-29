# _*_ coding: utf-8 _*_

"""
user page
"""

import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html

from models import DbMaker
from models.crud import crud_user
from ..comps import get_component_logo
from ..comps.header import get_component_header, get_component_header_user

TAG = "user"

# style of page
STYLE_PAGE = """
"""


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    user_id = kwargs.get("user_id")

    # user instance
    with DbMaker() as db:
        user_db = crud_user.get(db, _id=user_id)
    user_title = user_db.email.split("@")[0]

    # define components
    style = {"minHeight": "300px"}
    div_profile = html.Div("Profile", className="bg-white p-3", style=style)
    div_settings = html.Div("Settings", className="bg-white p-3", style=style)

    # return result
    return html.Div(children=[
        get_component_header(
            children_left=get_component_logo(size=20),
            children_right=get_component_header_user(user_title, dot=True),
        ),
        # define components
        fac.AntdTabs(children=[
            fac.AntdTabPane(div_profile, key="profile", tab="Profile"),
            fac.AntdTabPane(div_settings, key="settings", tab="Settings"),
        ], tabPosition="left", className="w-75 m-auto mt-4"),
        # define style of this page
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
        dcc.Store(id=f"id-{TAG}-uid", data=user_db.id),
    ], className="vh-100 overflow-auto")
