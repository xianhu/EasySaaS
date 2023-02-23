# _*_ coding: utf-8 _*_

"""
projects page
"""

import time

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
import flask_login
from dash import Input, Output, State, dcc, html

from app import app_db
from models.users import User
from utility.paths import PATH_ANALYSIS
from . import paddp, peditp, pdelp
from ..comps import header as comps_header

TAG = "projects"
COUNT_PROJECTS_MAX = 3


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # define components for add project
    modal_addp = paddp.layout(pathname, search)
    data_addp_open = dcc.Store(id=f"id-{TAG}-addp-open", data=0)
    data_addp_close = dcc.Store(id=f"id-{TAG}-addp-close", data=0)
    data_addp_pid = dcc.Store(id=f"id-{TAG}-addp-pid", data=None)

    # define components for edit project
    modal_editp = peditp.layout(pathname, search)
    data_editp_open = dcc.Store(id=f"id-{TAG}-editp-open", data=0)
    data_editp_close = dcc.Store(id=f"id-{TAG}-editp-close", data=0)
    data_editp_pid = dcc.Store(id=f"id-{TAG}-editp-pid", data=None)

    # define components for delete project
    modal_delp = pdelp.layout(pathname, search)
    data_delp_open = dcc.Store(id=f"id-{TAG}-delp-open", data=0)
    data_delp_close = dcc.Store(id=f"id-{TAG}-delp-close", data=0)
    data_delp_pid = dcc.Store(id=f"id-{TAG}-delp-pid", data=None)

    # define components
    button_add = fac.AntdButton("Add New Project", id=f"id-{TAG}-button-add", type="primary", disabled=True)
    col_list = [fac.AntdCol(html.Span("Project List"), className=None), fac.AntdCol(button_add, className=None)]

    # return result
    return html.Div(children=[
        # define components
        comps_header.get_component_header(user_title=user_title, dot=True),
        html.Div(children=[
            fac.AntdRow(col_list, align="bottom", justify="space-between"),
            html.Div(id=f"id-{TAG}-div-main", className="bg-white mt-2"),
        ], className="w-75 m-auto mt-4"),
        # define components of modal
        modal_addp, data_addp_open, data_addp_close, data_addp_pid,
        modal_editp, data_editp_open, data_editp_close, data_editp_pid,
        modal_delp, data_delp_open, data_delp_close, data_delp_pid,
        # define components of others
        dcc.Store(id=f"id-{TAG}-data-uid", data=current_user.id),
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
        fuc.FefferyStyle(rawStyle="""
            .ant-table-cell {
                padding: 20px !important;
            }
        """)
    ], className="bg-main vh-100 overflow-auto")


@dash.callback([
    Output(f"id-{TAG}-button-add", "disabled"),
    Output(f"id-{TAG}-div-main", "children"),
], [
    Input(f"id-{TAG}-addp-close", "data"),
    Input(f"id-{TAG}-editp-close", "data"),
    Input(f"id-{TAG}-delp-close", "data"),
    State(f"id-{TAG}-data-uid", "data"),
], prevent_initial_call=False)
def _update_page(_add, _edit, _del, user_id):
    # get user and projects_list
    user = app_db.session.query(User).get(user_id)
    projects_list = [p for p in user.projects if p.status == 1]

    # define data
    data_table = [{
        "key": project.id,
        "name": project.name,
        "desc": project.desc,
        "status": project.status,
        "operation": [
            {"content": "Detail", "type": "link", "href": f"{PATH_ANALYSIS}?id={project.id}"},
            {"content": "Edit", "type": "link"},
            {"content": "Delete", "type": "link", "danger": True},
        ]
    } for project in projects_list]

    # define components
    table_project = fac.AntdTable(id=f"id-{TAG}-table-project", columns=[
        {"title": "Name", "dataIndex": "name", "width": "20%"},
        {"title": "Description", "dataIndex": "desc", "width": "40%"},
        {"title": "Status", "dataIndex": "status", "width": "10%"},
        {"title": "Operation", "dataIndex": "operation", "width": "30%", "renderOptions": {"renderType": "button"}}
    ], data=data_table, locale="en-us", bordered=False, pagination=dict(hideOnSinglePage=True))

    # return result
    return False if len(projects_list) < COUNT_PROJECTS_MAX else True, table_project


@dash.callback([dict(
    open=Output(f"id-{TAG}-addp-open", "data"),
    pid=Output(f"id-{TAG}-addp-pid", "data"),
), dict(
    open=Output(f"id-{TAG}-editp-open", "data"),
    pid=Output(f"id-{TAG}-editp-pid", "data"),
), dict(
    open=Output(f"id-{TAG}-delp-open", "data"),
    pid=Output(f"id-{TAG}-delp-pid", "data"),
)], [
    Input(f"id-{TAG}-button-add", "nClicks"),
    Input(f"id-{TAG}-table-project", "nClicksButton"),
], [
    State(f"id-{TAG}-table-project", "clickedContent"),
    State(f"id-{TAG}-table-project", "recentlyButtonClickedRow"),
    State(f"id-{TAG}-data-uid", "data"),
], prevent_initial_call=True)
def _update_page(n_clicks, n_clicks_button, clicked_content, clicked_row, user_id):
    # define outputs
    out_addp = dict(open=dash.no_update, pid=None)
    out_editp = dict(open=dash.no_update, pid=None)
    out_delp = dict(open=dash.no_update, pid=None)

    # get user and projects instances
    user = app_db.session.query(User).get(user_id)
    projects_list = [p for p in user.projects if p.status == 1]
    projects_id_set = set([p.id for p in projects_list])

    # get triggered_id
    triggered_id = dash.ctx.triggered_id

    # check triggered_id
    if triggered_id == f"id-{TAG}-button-add":
        if len(projects_list) < COUNT_PROJECTS_MAX:
            out_addp["open"] = time.time()
            return out_addp, out_editp, out_delp

    # check triggered_id
    if triggered_id == f"id-{TAG}-table-project":
        # check clicked_content
        if clicked_content == "Edit":
            if clicked_row["key"] in projects_id_set:
                out_editp["open"] = time.time()
                out_editp["pid"] = clicked_row["key"]
                return out_addp, out_editp, out_delp

        # check hash for delete
        if clicked_content == "Delete":
            if clicked_row["key"] in projects_id_set:
                out_delp["open"] = time.time()
                out_delp["pid"] = clicked_row["key"]
                return out_addp, out_editp, out_delp

    # return result
    return out_addp, out_editp, out_delp
