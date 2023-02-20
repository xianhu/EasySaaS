# _*_ coding: utf-8 _*_

"""
projects page
"""

import time

import dash
import feffery_antd_components as fac
import flask_login
from dash import Input, Output, State, dcc, html

from app import app_db
from models.users import User, Project, ProjectUser
from utility import get_md5
from utility.paths import PATH_ANALYSIS
from ..comps import header as comps_header

TAG = "projects"


def _layout_projects(user_id):
    """
    layout of projects
    """
    # get projects
    user = app_db.session.query(User).get(user_id)
    projects_list = [p for p in user.projects if p.status == 1]

    # check projects
    if not projects_list:
        children = fac.AntdEmpty(description="No Project")
        return dict(children=children, disabled=False, hash="")

    # define components
    div_list = [fac.AntdRow(children=[
        fac.AntdCol(html.Span("Project Name", className="fw-bold"), span=5),
        fac.AntdCol(html.Span("Project Description", className="fw-bold"), span=12),
        fac.AntdCol(html.Span("Status", className="fw-bold"), span=2),
        fac.AntdCol(html.Span("Operation", className="fw-bold"), span=5),
    ]), fac.AntdDivider(className="my-3")]

    # define components
    for project in projects_list:
        div_list.append(fac.AntdRow(children=[
            fac.AntdCol(html.Span(project.name), span=5),
            fac.AntdCol(html.Span(project.desc), span=12),
            fac.AntdCol(html.Span(project.status), span=2),
            fac.AntdCol(children=[
                html.A("Detail", href=f"{PATH_ANALYSIS}?id={project.id}"),
                html.A("Edit", href=f"#edit#{project.id}", className="ms-3"),
                html.A("Delete", href=f"#delete#{project.id}", className="text-danger ms-3"),
            ], span=5),
        ]))
        div_list.append(fac.AntdDivider(className="my-3"))

    # return result
    disabled = False if len(projects_list) < 3 else True
    return dict(children=div_list, disabled=disabled, hash="")


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # define components for modal
    input_id = fac.AntdInput(id=f"id-{TAG}-input-id", className="d-none")
    form_id = fac.AntdFormItem(input_id, id=f"id-{TAG}-form-id", className="d-none")

    # define components for modal
    input_name = fac.AntdInput(id=f"id-{TAG}-input-name", placeholder="project name", size="large")
    form_name = fac.AntdFormItem(input_name, id=f"id-{TAG}-form-name", label="project name:", required=True)

    # define components for modal
    input_desc = fac.AntdInput(id=f"id-{TAG}-input-desc", placeholder="project description", size="large")
    form_desc = fac.AntdFormItem(input_desc, id=f"id-{TAG}-form-desc", label="project description:")

    # define components for modal
    form_item = fac.AntdForm([form_id, form_name, form_desc], layout="vertical")
    kwargs_modal = dict(
        title="Add New Project", visible=False, closable=False, maskClosable=False, renderFooter=True,
        okText="Add New Project", okClickClose=False, confirmAutoSpin=True, cancelText="Cancel",
    )

    # define components
    button_new = fac.AntdButton("Add New Project", id=f"id-{TAG}-button-new", type="primary")
    col_list = [fac.AntdCol(html.Span("Project List")), fac.AntdCol(button_new)]

    # return result
    return html.Div(children=[
        comps_header.get_component_header(user_title=user_title, dot=True),
        html.Div(children=[
            fac.AntdRow(col_list, align="bottom", justify="space-between"),
            html.Div(id=f"id-{TAG}-div-main", className="bg-white mt-2 p-4"),
        ], className="w-75 m-auto mt-4"),
        fac.AntdModal(form_item, id=f"id-{TAG}-modal-project", **kwargs_modal),
        dcc.Store(id=f"id-{TAG}-data-uid", data=current_user.id),
        dcc.Location(id=f"id-{TAG}-location-current", refresh=False),
    ], className="bg-main vh-100 overflow-auto")


@dash.callback([dict(
    value=Output(f"id-{TAG}-input-id", "value"),
), dict(
    value=Output(f"id-{TAG}-input-name", "value"),
    status=Output(f"id-{TAG}-form-name", "validateStatus"),
    help=Output(f"id-{TAG}-form-name", "help"),
), dict(
    value=Output(f"id-{TAG}-input-desc", "value"),
    status=Output(f"id-{TAG}-form-desc", "validateStatus"),
    help=Output(f"id-{TAG}-form-desc", "help"),
), dict(
    visible=Output(f"id-{TAG}-modal-project", "visible"),
    loading=Output(f"id-{TAG}-modal-project", "confirmLoading"),
), dict(
    children=Output(f"id-{TAG}-div-main", "children"),
    disabled=Output(f"id-{TAG}-button-new", "disabled"),
    hash=Output(f"id-{TAG}-location-current", "hash"),
)], [
    Input(f"id-{TAG}-button-new", "nClicks"),
    Input(f"id-{TAG}-modal-project", "okCounts"),
    Input(f"id-{TAG}-location-current", "hash"),
], [
    State(f"id-{TAG}-input-id", "value"),
    State(f"id-{TAG}-input-name", "value"),
    State(f"id-{TAG}-input-desc", "value"),
    State(f"id-{TAG}-data-uid", "data"),
], prevent_initial_call=False)
def _update_page(n_clicks, ok_counts, vhash, _id, name, desc, user_id):
    # define outputs
    out_id = dict(value=dash.no_update)
    out_name = dict(value=dash.no_update, status="", help="")
    out_desc = dict(value=dash.no_update, status="", help="")
    out_modal = dict(visible=dash.no_update, loading=False)
    out_others = dict(children=dash.no_update, disabled=False, hash="")

    # check trigger_id
    if not dash.ctx.triggered_id:
        out_others = _layout_projects(user_id)
        return out_id, out_name, out_desc, out_modal, out_others
    trigger_id = dash.ctx.triggered_id

    # check trigger_id
    if trigger_id == f"id-{TAG}-button-new":
        out_id["value"] = ""
        out_name["value"] = ""
        out_desc["value"] = ""
        out_modal["visible"] = True
        return out_id, out_name, out_desc, out_modal, out_others

    # check trigger_id
    if trigger_id == f"id-{TAG}-modal-project":
        # check project name
        name = (name or "").strip()
        if len(name) < 4:
            out_name["status"] = "error"
            out_name["help"] = "project name is too short"
            return out_id, out_name, out_desc, out_modal, out_others

        # check project name
        user = app_db.session.query(User).get(user_id)
        if (not _id) and (name in set([p.name for p in user.projects if p.status == 1])):
            out_name["status"] = "error"
            out_name["help"] = "project name already exists"
            return out_id, out_name, out_desc, out_modal, out_others

        if _id:
            # update project
            app_db.session.query(Project).filter(Project.id == _id).update({
                "name": name, "desc": (desc or "").strip(),
            })
        else:
            # add new project
            _id = get_md5(user_id + name + str(time.time()))
            project = Project(id=_id, name=name, desc=(desc or "").strip())
            project_user = ProjectUser(user_id=user.id, project_id=project.id)
            app_db.session.add_all([project, project_user])

        # commit to database
        app_db.session.commit()

        # update page
        out_modal["visible"] = False
        out_others = _layout_projects(user_id)
        return out_id, out_name, out_desc, out_modal, out_others

    # check trigger_id
    if trigger_id == f"id-{TAG}-location-current":
        operation, _id = [item for item in vhash.strip("#").split("#")]
        project = app_db.session.query(Project).get(_id)

        # delete project
        if operation == "delete":
            project.status = 0
            app_db.session.commit()

            # update page
            out_others = _layout_projects(user_id)
            return out_id, out_name, out_desc, out_modal, out_others

        # edit project
        if operation == "edit":
            out_id["value"] = project.id
            out_name["value"] = project.name
            out_desc["value"] = project.desc
            out_modal["visible"] = True
            return out_id, out_name, out_desc, out_modal, out_others

    # return result (default)
    return out_id, out_name, out_desc, out_modal, out_others
