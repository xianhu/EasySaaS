# _*_ coding: utf-8 _*_

"""
new project page
"""

import time

import dash
import feffery_antd_components as fac
from dash import Input, Output, State, dcc, html

from app import app_db
from models.users import User, Project, ProjectUser
from utility import get_md5

TAG_BASE = "project"
TAG = "project-newp"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    input_name = fac.AntdInput(id=f"id-{TAG}-input-name", placeholder="project name", size="large")
    form_name = fac.AntdFormItem(input_name, id=f"id-{TAG}-form-name", label="project name:")

    # define components
    input_desc = fac.AntdInput(id=f"id-{TAG}-input-desc", placeholder="project description", size="large")
    form_desc = fac.AntdFormItem(input_desc, id=f"id-{TAG}-form-desc", label="project description:")

    # define components
    data_uid = dcc.Store(id=f"id-{TAG}-data-uid", data=kwargs["user_id"])
    form_project = fac.AntdForm([form_name, form_desc, data_uid], layout="vertical")

    # return result
    return fac.AntdModal(
        form_project, id=f"id-{TAG}-modal-new", visible=False,
        closable=False, maskClosable=False, renderFooter=True,
        okText="Add New Project", okClickClose=False, confirmAutoSpin=True,
        cancelText="Cancel", title=html.Span("Add New Project"),
    )


@dash.callback([dict(
    visible=Output(f"id-{TAG}-modal-new", "visible"),
    loading=Output(f"id-{TAG}-modal-new", "confirmLoading"),
), dict(
    value=Output(f"id-{TAG}-input-name", "value"),
    status=Output(f"id-{TAG}-form-name", "validateStatus"),
    help=Output(f"id-{TAG}-form-name", "help"),
), dict(
    value=Output(f"id-{TAG}-input-desc", "value"),
    status=Output(f"id-{TAG}-form-desc", "validateStatus"),
    help=Output(f"id-{TAG}-form-desc", "help"),
), Output(f"id-{TAG_BASE}-data-newp", "data")], [
    Input(f"id-{TAG_BASE}-button-new", "nClicks"),
    Input(f"id-{TAG}-modal-new", "okCounts"),
    State(f"id-{TAG}-input-name", "value"),
    State(f"id-{TAG}-input-desc", "value"),
    State(f"id-{TAG}-data-uid", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, ok_counts, name, desc, user_id):
    # define outputs
    out_modal = dict(visible=dash.no_update, loading=False)
    out_name = dict(value=dash.no_update, status="", help="")
    out_desc = dict(value=dash.no_update, status="", help="")
    out_data_newp = dash.no_update

    # check trigger
    trigger_id = dash.ctx.triggered_id
    if trigger_id == f"id-{TAG_BASE}-button-new":
        out_modal["visible"] = True
        out_name["value"] = ""
        out_desc["value"] = ""
        return out_modal, out_name, out_desc, out_data_newp

    # check trigger
    if trigger_id == f"id-{TAG}-modal-new":
        name = (name or "").strip()
        if not name:
            out_name["status"] = "error"
            out_name["help"] = "project name is required"
            return out_modal, out_name, out_desc, out_data_newp

        desc = (desc or "").strip()
        if not desc:
            out_desc["status"] = "error"
            out_desc["help"] = "project description is required"
            return out_modal, out_name, out_desc, out_data_newp

        # check project name
        user = app_db.session.query(User).get(user_id)
        for project in user.projects:
            if project.name == name:
                out_name["status"] = "error"
                out_name["help"] = "project name already exists"
                return out_modal, out_name, out_desc, out_data_newp

        # add new project
        project_id = get_md5(user_id + name)
        project = Project(id=project_id, name=name, desc=desc)
        project_user = ProjectUser(project_id=project_id, user_id=user_id)

        # add to database
        app_db.session.add_all([project, project_user])
        app_db.session.commit()

    # return result
    out_modal["visible"] = False
    out_data_newp = int(time.time())
    return out_modal, out_name, out_desc, out_data_newp
