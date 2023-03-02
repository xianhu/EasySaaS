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
from models.users import Project, UserProject
from utility.paths import PATH_ANALYSIS
from . import paddedit, pdelete
from ..comps import header as comps_header

TAG = "projects"

# define style
STYLE_PAGE = """
.ant-table .ant-btn {font-size: 16px !important;}
.ant-table .ant-table-cell {font-size: 16px !important; padding: 20px !important;}
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
        modal_addedit, data_addedit_open, data_addedit_close, data_addedit_project,
        modal_delete, data_delete_open, data_delete_close, data_delete_project,
        # define components of others
        dcc.Store(id=f"id-{TAG}-data-uid", data=current_user.id),
        fuc.FefferyStyle(rawStyle=STYLE_PAGE)
    ], className="bg-main vh-100 overflow-auto")


@dash.callback([
    Output(f"id-{TAG}-button-add", "disabled"),
    Output(f"id-{TAG}-div-main", "children"),
], [
    Input(f"id-{TAG}-addedit-close", "data"),
    Input(f"id-{TAG}-delete-close", "data"),
    State(f"id-{TAG}-data-uid", "data"),
], prevent_initial_call=False)
def _update_page(addedit, delete, user_id):
    # get project_role_list (all projects)
    project_role_list = app_db.session.query(Project, UserProject.role).join(
        UserProject, UserProject.project_id == Project.id,
    ).filter(
        UserProject.user_id == user_id,
        UserProject.status == 1,
        Project.status == 1,
    ).all()

    # define data
    data_table = []
    for project, project_role in project_role_list:
        href_analysis = f"{PATH_ANALYSIS}?id={project.id}"
        operation = [{"content": "Analysis", "type": "link", "href": href_analysis}]
        if project_role == "admin":
            operation.append({"content": "Edit", "type": "link"})
            operation.append({"content": "Delete", "type": "link", "danger": True})
        data_table.append({
            "key": project.id,
            "name": project.name,
            "desc": project.desc,
            "role": project_role,
            "operation": operation,
        })

    # define components
    table_project = fac.AntdTable(id=f"id-{TAG}-table-project", columns=[
        {"title": "Name", "dataIndex": "name", "width": "20%"},
        {"title": "Description", "dataIndex": "desc", "width": "40%"},
        {"title": "Role", "dataIndex": "role", "width": "10%"},
        {"title": "Operation", "dataIndex": "operation", "width": "30%", "renderOptions": {"renderType": "button"}}
    ], data=data_table, bordered=False, pagination=dict(hideOnSinglePage=True), locale="en-us")

    # return result
    return False, table_project


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
    out_addedit = dict(open=dash.no_update, project=None)
    out_delete = dict(open=dash.no_update, project=None)

    # get triggered_id
    triggered_id = dash.ctx.triggered_id

    # check triggered_id
    if triggered_id == f"id-{TAG}-button-add":
        out_addedit["open"] = time.time()
        out_addedit["project"] = None
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
