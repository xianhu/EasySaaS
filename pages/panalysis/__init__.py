# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
import flask_login
from dash import Input, Output, State

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
            fac.AntdCol(id=f"id-{TAG}-header", className="fs-6"),
            fac.AntdCol(fac.AntdBadge(fac.AntdDropdown(menuItems=[
                {"title": "Profile", "key": "Profile"},
                {"title": "Settings", "key": "Settings"},
                {"isDivider": True},
                {"title": "Logout", "href": "/login"},
            ], id=f"id-{TAG}-user", title=user_title, buttonMode=True), dot=True)),
        ], align="middle", justify="space-between", className="bg-white sticky-top px-4 py-2"),
        fuc.FefferyTopProgress(fac.AntdContent(id=f"id-{TAG}-content", className="px-4 py-4")),
        fuc.FefferyWindowSize(id=f"id-{TAG}-window-size"),
    ], className="vh-100 overflow-auto")

    # return result
    return fac.AntdLayout([sider, content], className="vh-100 overflow-auto")


@dash.callback([
    Output(f"id-{TAG}-menu", "currentKey"),
    Output(f"id-{TAG}-user", "clickedKey"),
    Output(f"id-{TAG}-header", "children"),
    Output(f"id-{TAG}-content", "children"),
], [
    Input(f"id-{TAG}-menu", "currentKey"),
    Input(f"id-{TAG}-user", "clickedKey"),
    State(f"id-{TAG}-window-size", "_width"),
    State(f"id-{TAG}-window-size", "_height"),
], prevent_initial_call=False)
def _update_content(current_key, clicked_key, width, height):
    # check trigger
    trigger_id = dash.ctx.triggered_id
    if not trigger_id:
        trigger_id = f"id-{TAG}-menu"
        current_key = ROUTER_MENU[0]["props"]["key"]

    # define components
    if trigger_id == f"id-{TAG}-menu":
        # current_key = current_key
        header = f"{current_key}({width}x{height})"
        content = fac.AntdEmpty(locale="en_US")
    else:
        current_key = None
        header = f"{clicked_key}({width}x{height})"
        content = fac.AntdEmpty(locale="en_US")

    # return result
    return current_key, None, header, content
