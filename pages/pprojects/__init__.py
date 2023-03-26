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

from utility.paths import PATH_ANALYSIS
from . import paddedit, pdelete
from ..comps import header as comps_header

TAG = "projects"

# style of page
STYLE_PAGE = """
    .ant-table .ant-btn {
        font-size: 16px !important;
    }
    .ant-table .ant-table-cell {
        font-size: 16px !important; 
        padding: 20px !important;
    }
"""


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # define components for (addedit) project
    modal_addedit = paddedit.layout(pathname, search)
    data_addedit_open = dcc.Store(id=f"id-{TAG}-addedit-open", data=0)
    data_addedit_close = dcc.Store(id=f"id-{TAG}-addedit-close", data=0)
    data_addedit_project = dcc.Store(id=f"id-{TAG}-addedit-project", data=None)

    # define components for (delete) project
    modal_delete = pdelete.layout(pathname, search)
    data_delete_open = dcc.Store(id=f"id-{TAG}-delete-open", data=0)
    data_delete_close = dcc.Store(id=f"id-{TAG}-delete-close", data=0)
    data_delete_project = dcc.Store(id=f"id-{TAG}-delete-project", data=None)

    # define components
    button_add = fac.AntdButton("Add Project", id=f"id-{TAG}-button-add", type="primary", disabled=True)
    col_list = [fac.AntdCol(html.Span("Project List", className=None)), fac.AntdCol(button_add)]

    # return result
    return html.Div(children=[
        # define components
        comps_header.get_component_header(user_title=user_title, dot=True),
        html.Div(children=[
            fac.AntdRow(col_list, align="bottom", justify="space-between"),
            fac.AntdSpin(html.Div(id=f"id-{TAG}-div-table", className="mt-2")),
        ], className="w-75 m-auto mt-4"),
        # define components of modal
        modal_addedit, data_addedit_open, data_addedit_close, data_addedit_project,
        modal_delete, data_delete_open, data_delete_close, data_delete_project,
        # define components of others
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
    ], className="bg-main vh-100 overflow-auto")


@dash.callback([
    Output(f"id-{TAG}-button-add", "disabled"),
    Output(f"id-{TAG}-div-table", "children"),
], [
    Input(f"id-{TAG}-addedit-close", "data"),
    Input(f"id-{TAG}-delete-close", "data"),
], prevent_initial_call=False)
def _update_page(data_addedit, data_delete):
    # user instance
    current_user = flask_login.current_user

    # table data
    data_table = []
    for up in current_user.user_projects:
        if up.project.status == 0:
            continue
        up_role = up.role
        project = up.project

        # define operation of button column
        href = f"{PATH_ANALYSIS}?id={project.id}"
        operation = [{"content": "Analysis", "type": "link", "href": href}]
        if up_role == "admin":
            operation.append({"content": "Edit", "type": "link"})
            operation.append({"content": "Delete", "type": "link", "danger": True})

        # append data
        data_table.append({
            "id": project.id, "key": project.id,
            "name": project.name, "desc": project.desc,
            "role": up_role, "operation": operation,
        })

    # return result
    return False, fac.AntdTable(id=f"id-{TAG}-table-project", columns=[
        {"title": "Name", "dataIndex": "name", "width": "20%"},
        {"title": "Description", "dataIndex": "desc", "width": "40%", "renderOptions": {"renderType": "ellipsis"}},
        {"title": "Role", "dataIndex": "role", "width": "10%"},
        {"title": "Operation", "dataIndex": "operation", "width": "30%", "renderOptions": {"renderType": "button"}},
    ], data=data_table, bordered=False, emptyContent="No Projects", pagination=dict(pageSize=10, hideOnSinglePage=True))


@dash.callback([dict(
    open=Output(f"id-{TAG}-addedit-open", "data"),
    project=Output(f"id-{TAG}-addedit-project", "data"),
), dict(
    open=Output(f"id-{TAG}-delete-open", "data"),
    project=Output(f"id-{TAG}-delete-project", "data"),
)], [
    Input(f"id-{TAG}-button-add", "nClicks"),
    Input(f"id-{TAG}-table-project", "nClicksButton"),
], [
    State(f"id-{TAG}-table-project", "clickedContent"),
    State(f"id-{TAG}-table-project", "recentlyButtonClickedRow"),
], prevent_initial_call=True)
def _update_page(n_clicks, n_clicks_table, clicked_content, clicked_row):
    # define outputs
    out_addedit = dict(open=dash.no_update, project=dash.no_update)
    out_delete = dict(open=dash.no_update, project=dash.no_update)

    # get triggered_id
    triggered_id = dash.ctx.triggered_id

    # check triggered_id
    if triggered_id == f"id-{TAG}-button-add":
        out_addedit["open"] = time.time()
        out_addedit["project"] = dict()
        return out_addedit, out_delete

    # check triggered_id
    if triggered_id == f"id-{TAG}-table-project" and clicked_content == "Edit":
        out_addedit["open"] = time.time()
        out_addedit["project"] = clicked_row
        return out_addedit, out_delete

    # check triggered_id
    if triggered_id == f"id-{TAG}-table-project" and clicked_content == "Delete":
        out_delete["open"] = time.time()
        out_delete["project"] = clicked_row
        return out_addedit, out_delete

    # return result
    return out_addedit, out_delete
