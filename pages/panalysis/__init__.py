# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash
import feffery_antd_components as fac
import flask_login
from dash import Input, Output

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
            fac.AntdCol(fac.AntdDropdown(menuItems=[
                {"title": "Profile", "key": "Profile"},
                {"title": "Settings", "key": "Settings"},
                {"isDivider": True},
                {"title": "Logout", "href": "/login"},
            ], id=f"id-{TAG}-user", title=user_title, buttonMode=True)),
        ], align="middle", justify="space-between", className="bg-white px-4 py-2"),
        fac.AntdContent(id=f"id-{TAG}-content", className="px-4 py-4"),
    ], className="vh-100 overflow-auto")

    # return result
    return fac.AntdLayout([sider, content], className="vh-100 overflow-auto")


@dash.callback([
    Output(f"id-{TAG}-menu", "currentKey"),
    Output(f"id-{TAG}-menu", "openKeys"),
    Output(f"id-{TAG}-header", "children"),
    Output(f"id-{TAG}-content", "children"),
], [
    Input(f"id-{TAG}-menu", "currentKey"),
    Input(f"id-{TAG}-user", "clickedKey"),
], prevent_initial_call=False)
def _update_content(current_key, clicked_key):
    # check trigger
    trigger_id = dash.ctx.triggered_id
    if not trigger_id:
        current_key = ROUTER_MENU[0]["props"]["key"]

    # define components
    empty = fac.AntdEmpty(locale="en_US", description="No Content")

    # return result
    if (not trigger_id) or (trigger_id == f"id-{TAG}-menu"):
        return current_key, dash.no_update, current_key, empty
    else:
        return None, None, clicked_key, empty
