# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
import flask_login
from dash import Input, Output, State

from utility.consts import FMT_EXECUTEJS_HREF
from utility.paths import PATH_LOGIN
from .routers import ROUTER_MENU

TAG = "analysis"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    user = flask_login.current_user
    user_title = user.email.split("@")[0]

    # define components
    menu = fac.AntdMenu(id=f"id-{TAG}-menu", menuItems=ROUTER_MENU, mode="inline", theme="dark")
    sider = fac.AntdSider(children=menu, collapsible=True, theme="dark", className="vh-100 overflow-auto")

    # define components
    content = fac.AntdContent(children=[
        fac.AntdRow(children=[
            fac.AntdCol(id=f"id-{TAG}-header", className="fs-6 fw-bold"),
            fac.AntdCol(fac.AntdBadge(fac.AntdDropdown(menuItems=[
                {"title": "Profile", "key": "Profile"},
                {"title": "Settings", "key": "Settings"},
                {"isDivider": True},
                {"title": "Logout", "href": "/login"},
            ], id=f"id-{TAG}-user", title=user_title, buttonMode=True), dot=True)),
        ], align="middle", justify="space-between", className="bg-white sticky-top px-4 py-2"),
        fuc.FefferyTopProgress(fac.AntdContent(id=f"id-{TAG}-content", className="px-4 py-4")),
        # define components
        fuc.FefferyWindowSize(id=f"id-{TAG}-windowsize"),
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
    ], className="vh-100 overflow-auto")

    # return result
    return fac.AntdLayout([sider, content], className="vh-100 overflow-auto")


@dash.callback([dict(
    current_key=Output(f"id-{TAG}-menu", "currentKey"),
    clicked_key=Output(f"id-{TAG}-user", "clickedKey"),
), dict(
    header=Output(f"id-{TAG}-header", "children"),
    content=Output(f"id-{TAG}-content", "children"),
), Output(f"id-{TAG}-executejs", "jsString"),
], [
    Input(f"id-{TAG}-menu", "currentKey"),
    Input(f"id-{TAG}-user", "clickedKey"),
    State(f"id-{TAG}-windowsize", "_width"),
    State(f"id-{TAG}-windowsize", "_height"),
], prevent_initial_call=False)
def _update_content(current_key, clicked_key, width, height):
    # define outputs
    out_key = dict(current_key=current_key, clicked_key=None)
    out_content = dict(header="", content=fac.AntdEmpty(locale="en_US"))
    out_executejs = dash.no_update

    # check user
    user = flask_login.current_user
    if not user.is_authenticated:
        out_executejs = FMT_EXECUTEJS_HREF.format(PATH_LOGIN)
        return out_key, out_content, out_executejs

    # check trigger
    trigger_id = dash.ctx.triggered_id
    if not trigger_id:
        trigger_id = f"id-{TAG}-menu"
        current_key = ROUTER_MENU[0]["props"]["key"]

    # define components
    if trigger_id == f"id-{TAG}-menu":
        out_key["current_key"] = current_key
        out_content["header"] = f"{current_key}({width}x{height})"
    else:
        out_key["current_key"] = None
        out_content["header"] = f"{clicked_key}({width}x{height})"

    # return result
    return out_key, out_content, out_executejs
