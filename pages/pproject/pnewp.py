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
    data_uid = dcc.Store(id=f"id-{TAG}-data-uid", data=kwargs["user_id"])

    # define components
    input_name = fac.AntdInput(id=f"id-{TAG}-input-name", placeholder="project name", size="large")
    form_name = fac.AntdFormItem(input_name, id=f"id-{TAG}-form-name", required=True, label="project name:")

    # define components
    input_desc = fac.AntdInput(id=f"id-{TAG}-input-desc", placeholder="project description", size="large")
    form_desc = fac.AntdFormItem(input_desc, id=f"id-{TAG}-form-desc", required=True, label="project description:")

    # return result
    return fac.AntdModal(
        fac.AntdForm([form_name, form_desc, data_uid], layout="vertical"),
        id=f"id-{TAG}-modal-new", title=html.Span("Add New Project"),
        visible=False, closable=False, maskClosable=False, renderFooter=True,
        okText="Add New Project", okClickClose=False, confirmAutoSpin=True, cancelText="Cancel",
    )


@dash.callback([dict(
    visible=Output(f"id-{TAG}-modal-new", "visible"),
    loading=Output(f"id-{TAG}-modal-new", "confirmLoading"),
), dict(
    status=Output(f"id-{TAG}-form-name", "validateStatus"),
    help=Output(f"id-{TAG}-form-name", "help"),
    value=Output(f"id-{TAG}-input-name", "value"),
), dict(
    status=Output(f"id-{TAG}-form-desc", "validateStatus"),
    help=Output(f"id-{TAG}-form-desc", "help"),
    value=Output(f"id-{TAG}-input-desc", "value"),
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
    out_name = dict(status="", help="", value=dash.no_update)
    out_desc = dict(status="", help="", value=dash.no_update)
    out_data_newp = dash.no_update

    # check trigger
    trigger_id = dash.ctx.triggered_id
    if trigger_id == f"id-{TAG_BASE}-button-new":
        out_modal["visible"] = True
        out_name = dict(status="", help="", value="")
        out_desc = dict(status="", help="", value="")
        return out_modal, out_name, out_desc, out_data_newp

    # check trigger
    if trigger_id == f"id-{TAG}-modal-new":
        desc = (desc or "").strip()

        # check project name
        name = (name or "").strip()
        if len(name) < 4:
            out_name["status"] = "error"
            out_name["help"] = "project name is too short"
            return out_modal, out_name, out_desc, out_data_newp

        # check project name
        user = app_db.session.query(User).get(user_id)
        if name in set([project.name for project in user.projects]):
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
