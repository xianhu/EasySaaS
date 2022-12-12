# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
import flask_login
from dash import Input, Output, State, dcc, html

from .routers import ROUTER_MENU

TAG = "analysis"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    user = flask_login.current_user
    user_title = user.email.split("@")[0]
    store_data = dict(
        pathname=pathname, search=search,
        user_id=user.id, user_email=user.email,
    )

    # define components
    sider = fac.AntdSider(children=[
        fac.AntdMenu(id=f"id-{TAG}-menu", menuItems=ROUTER_MENU, mode="inline", theme="dark"),
    ], collapsible=True, theme="dark", className="vh-100 overflow-auto")

    # define components
    content = fac.AntdContent(children=[
        fac.AntdRow(children=[
            fac.AntdCol(id=f"id-{TAG}-header", className="fs-6 fw-bold"),
            fac.AntdCol(children=[
                fac.AntdSwitch(
                    id=f"id-{TAG}-switch",
                    checkedChildren="Open",
                    unCheckedChildren="Close",
                    className="me-2",
                ),
                fac.AntdBadge(fac.AntdDropdown(menuItems=[
                    {"title": "Profile", "key": "Profile"},
                    {"title": "Settings", "key": "Settings"},
                    {"isDivider": True},
                    {"title": "Logout", "href": "/login"},
                ], id=f"id-{TAG}-user", title=user_title, buttonMode=True), dot=True),
            ], className=None),
        ], align="middle", justify="space-between", className="bg-white sticky-top px-4 py-2"),
        fuc.FefferyTopProgress(children=[
            html.Div(id=f"id-{TAG}-content", className="px-4 py-4"),
        ], listenPropsMode="include", includeProps=[f"id-{TAG}-content.children"]),
    ], className="vh-100 overflow-auto")

    # return result
    return fac.AntdLayout(children=[
        sider, content,
        # define components
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
        fuc.FefferyWindowSize(id=f"id-{TAG}-windowsize"),
        dcc.Store(id=f"id-{TAG}-data", data=store_data),
    ], className="vh-100 overflow-auto")


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
    Input(f"id-{TAG}-switch", "checked"),
    State(f"id-{TAG}-windowsize", "_width"),
    State(f"id-{TAG}-windowsize", "_height"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=False)
def _update_content(current_key, clicked_key, switch_checked, _width, _height, store_data):
    # check trigger (default)
    trigger_id = dash.ctx.triggered_id
    if not trigger_id:
        trigger_id = f"id-{TAG}-menu"
        current_key = ROUTER_MENU[0]["props"]["key"]

    # define components
    if (trigger_id == f"id-{TAG}-switch" and current_key) or \
            trigger_id == f"id-{TAG}-menu":
        clicked_key = None
    elif (trigger_id == f"id-{TAG}-switch" and clicked_key) or \
            trigger_id == f"id-{TAG}-user":
        current_key = None
    out_key = dict(current_key=current_key, clicked_key=clicked_key)

    # define components
    header = f"{current_key}-{clicked_key}-{switch_checked}({_width}x{_height})"
    out_content = dict(header=header, content=fac.AntdEmpty(locale="en_US"))

    # return result
    return out_key, out_content, dash.no_update
