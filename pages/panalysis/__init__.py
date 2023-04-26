# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import Input, Output, State, dcc, html

from models import DbMaker
from models.crud import crud_project, crud_user
from . import pecharts, ptasks, pupload
from .routers import ROUTER_MENU
from .. import palert
from ..comps.header import get_component_header, get_component_header_user

TAG = "analysis"

# style of page
STYLE_PAGE = """
    .ant-menu-item-icon {
        display: flex !important;
    }
"""


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    project_id = int(search["id"][0])

    # user instance
    with DbMaker() as db:
        user_id = kwargs.get("user_id")
        user_db = crud_user.get(db, _id=user_id)
        project_db = crud_project.get(db, _id=project_id)
    user_title = user_db.email.split("@")[0]

    # check if project is exist
    if (not project_db) or (project_db.user_id != user_id):
        return palert.layout_expired(pathname, search)
    store_data = dict(user_id=user_db.id, project_id=project_db.id, project_name=project_db.name)

    # define components
    menu = fac.AntdMenu(id=f"id-{TAG}-menu", menuItems=ROUTER_MENU, mode="inline", theme="dark")
    sider = fac.AntdSider([menu, ], collapsible=True, theme="dark", className="vh-100 overflow-auto")

    # define components
    main = fac.AntdContent(children=[
        get_component_header(
            children_left=html.Div("Loading...", id=f"id-{TAG}-header"),
            children_right=get_component_header_user(user_title, dot=True),
        ),
        fuc.FefferyTopProgress(children=[
            html.Div(id=f"id-{TAG}-content"),
        ], listenPropsMode="include", includeProps=[f"id-{TAG}-content.children", ]),
    ], className="vh-100 overflow-auto")

    # return result
    return fac.AntdLayout(children=[
        sider, main,
        # define components of others
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
        dcc.Store(id=f"id-{TAG}-data", data=store_data),
        # define style of this page
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
    ], className="vh-100 overflow-auto")


@dash.callback([dict(
    header=Output(f"id-{TAG}-header", "children"),
    content=Output(f"id-{TAG}-content", "children"),
), dict(
    current_key=Output(f"id-{TAG}-menu", "currentKey"),
    executejs_string=Output(f"id-{TAG}-executejs", "jsString"),
)], [
    Input(f"id-{TAG}-menu", "currentKey"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=False)
def _update_page(current_key, store_data):
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
    text_title = f"{current_key}-{project_name}"
    out_main["header"] = fac.AntdTitle(text_title, level=4, className="m-0")

    # define content of main
    if current_key == "Echarts":
        out_main["content"] = pecharts.layout(None, None)
    elif current_key == "Upload":
        out_main["content"] = pupload.layout(None, None)
    elif current_key == "Tasks":
        out_main["content"] = ptasks.layout(None, None)

    # return result
    return out_main, out_others
