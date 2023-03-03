# _*_ coding: utf-8 _*_

"""
analysis page
"""

import logging
import urllib.parse

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
import flask_login
from dash import Input, Output, State, dcc, html

from . import pintros
from .routers import ROUTER_MENU
from .. import palert
from ..comps import header as comps_header

TAG = "analysis"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # get project_role_dict
    up_list = [up for up in current_user.user_projects if up.project.status == 1]
    project_role_dict = {up.project.id: (up.role, up.project) for up in up_list}

    # check project id
    try:
        search = urllib.parse.parse_qs(search.lstrip("?").strip())
        assert search["id"][0] in project_role_dict, "project not found"
    except Exception as excep:
        logging.error("get project.id failed: %s", excep)
        return palert.layout_500(pathname, search)
    project_id = search["id"][0]
    project_role, project = project_role_dict[project_id]

    # define store_data
    store_data = dict(
        user_id=current_user.id,
        project_id=project_id,
        project_role=project_role,
        project_name=project.name,
    )

    # define components
    menu = fac.AntdMenu(id=f"id-{TAG}-menu", menuItems=ROUTER_MENU, mode="inline", theme="dark")
    sider = fac.AntdSider([menu, ], collapsible=True, theme="dark", className="vh-100 overflow-auto")

    # define components
    kwargs_switch = dict(checkedChildren="Open", unCheckedChildren="Close")
    switch = fac.AntdSwitch(id=f"id-{TAG}-switch", **kwargs_switch, className="me-2")
    dropdown_user = comps_header.get_component_header_user(user_title, dot=True)

    # define components
    main = fac.AntdContent(children=[
        comps_header.get_component_header(
            chilren_left=html.Div("Analysis", id=f"id-{TAG}-header"),
            children_right=[switch, dropdown_user],
        ),
        fuc.FefferyTopProgress(children=[
            html.Div(id=f"id-{TAG}-content", className="px-4 py-4"),
        ], listenPropsMode="include", includeProps=[f"id-{TAG}-content.children"]),
    ], className="vh-100 overflow-auto")

    # return result
    return fac.AntdLayout(children=[
        sider, main,
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
        dcc.Store(id=f"id-{TAG}-data", data=store_data),
    ], className="bg-main vh-100 overflow-auto")


@dash.callback([dict(
    header=Output(f"id-{TAG}-header", "children"),
    content=Output(f"id-{TAG}-content", "children"),
), dict(
    current_key=Output(f"id-{TAG}-menu", "currentKey"),
    executejs_string=Output(f"id-{TAG}-executejs", "jsString"),
)], [
    Input(f"id-{TAG}-menu", "currentKey"),
    Input(f"id-{TAG}-switch", "checked"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=False)
def _update_page(current_key, switch_checked, store_data):
    # define outputs
    out_main = dict(header=dash.no_update, content=fac.AntdEmpty(locale="en-us"))
    out_others = dict(current_key=current_key, executejs_string=dash.no_update)

    # check triggered_id and current_key
    triggered_id = dash.ctx.triggered_id
    if not triggered_id:
        triggered_id = f"id-{TAG}-menu"
        current_key = ROUTER_MENU[0]["props"]["key"]
    out_others["current_key"] = current_key

    # define header of main
    project_name = store_data["project_name"]
    project_role = store_data["project_role"]
    text_title = f"{current_key}-{switch_checked}-{project_name}-{project_role}"
    out_main["header"] = fac.AntdTitle(text_title, level=4, className="m-0")

    # define content of main
    if triggered_id == f"id-{TAG}-menu":
        if current_key == "Intros":
            out_main["content"] = pintros.layout(None, None)

    # return result
    return out_main, out_others
