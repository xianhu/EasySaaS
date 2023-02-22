# _*_ coding: utf-8 _*_

"""
edit project
"""

import time

import dash
import feffery_antd_components as fac
from dash import Input, Output, State

from app import app_db
from models.users import Project

TAG_BASE = "projects"
TAG = "projects-editp"
TYPE = "editp"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    input_name = fac.AntdInput(id=f"id-{TAG}-input-name", placeholder="project name", size="large", readOnly=True)
    form_name = fac.AntdFormItem(input_name, id=f"id-{TAG}-form-name", label="project name:", required=True)

    # define components
    input_desc = fac.AntdInput(id=f"id-{TAG}-input-desc", placeholder="project description", size="large")
    form_desc = fac.AntdFormItem(input_desc, id=f"id-{TAG}-form-desc", label="project description:", required=False)

    # define components
    form_item = fac.AntdForm([form_name, form_desc], layout="vertical")
    kwargs_modal = dict(
        title="Update Project", visible=False, closable=False, maskClosable=False, renderFooter=True,
        okText="Update Project", okClickClose=False, confirmAutoSpin=True, cancelText="Cancel",
    )

    # return result
    return fac.AntdModal(form_item, id=f"id-{TAG}-modal-project", **kwargs_modal)


@dash.callback([dict(
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
    close=Output(f"id-{TAG_BASE}-{TYPE}-close", "data"),
)], [
    Input(f"id-{TAG_BASE}-{TYPE}-open", "data"),
    Input(f"id-{TAG}-modal-project", "okCounts"),
    State(f"id-{TAG}-input-name", "value"),
    State(f"id-{TAG}-input-desc", "value"),
    State(f"id-{TAG_BASE}-{TYPE}-pid", "data"),
    State(f"id-{TAG_BASE}-data-uid", "data"),
], prevent_initial_call=True)
def _update_page(_open_data, _ok_counts, name, desc, project_id, user_id):
    # define outputs
    out_name = dict(value=dash.no_update, status="", help="")
    out_desc = dict(value=dash.no_update, status="", help="")
    out_modal = dict(visible=dash.no_update, loading=False)
    out_others = dict(close=dash.no_update)

    # get user and project
    # user = app_db.session.query(User).get(user_id)
    project = app_db.session.query(Project).get(project_id)

    # check trigger_id
    trigger_id = dash.ctx.triggered_id
    if trigger_id == f"id-{TAG_BASE}-{TYPE}-open":
        out_name["value"] = project.name
        out_desc["value"] = project.desc
        out_modal["visible"] = True
        return out_name, out_desc, out_modal, out_others

    # check trigger_id
    if trigger_id == f"id-{TAG}-modal-project":
        project.desc = (desc or "").strip()
        app_db.session.commit()

        # update page
        out_modal["visible"] = False
        out_others["close"] = time.time()
        return out_name, out_desc, out_modal, out_others

    # return result
    return out_name, out_desc, out_modal, out_others
