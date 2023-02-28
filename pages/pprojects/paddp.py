# _*_ coding: utf-8 _*_

"""
add project
"""

import time

import dash
import feffery_antd_components as fac
from dash import Input, Output, State

from app import app_db
from models.users import User, Project, ProjectUser
from utility import get_md5

TAG_BASE = "projects"
TAG = "projects-addp"
TYPE = "addp"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    input_name = fac.AntdInput(id=f"id-{TAG}-input-name", placeholder="project name", size="large")
    form_name = fac.AntdFormItem(input_name, id=f"id-{TAG}-form-name", label="project name:", required=True)

    # define components
    input_desc = fac.AntdInput(id=f"id-{TAG}-input-desc", placeholder="project description", size="large")
    form_desc = fac.AntdFormItem(input_desc, id=f"id-{TAG}-form-desc", label="project description:", required=False)

    # define components
    form_item = fac.AntdForm([form_name, form_desc], layout="vertical")
    kwargs_modal = dict(
        title="Add New Project", visible=False, closable=False, renderFooter=True,
        okText="Add New Project", cancelText="Cancel", okClickClose=False, confirmAutoSpin=True,
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
], [
    State(f"id-{TAG}-input-name", "value"),
    State(f"id-{TAG}-input-desc", "value"),
    State(f"id-{TAG_BASE}-{TYPE}-pid", "data"),
    State(f"id-{TAG_BASE}-data-uid", "data"),
], prevent_initial_call=True)
def _update_page(open_data, ok_counts, name, desc, project_id, user_id):
    # define outputs
    out_name = dict(value=dash.no_update, status="", help="")
    out_desc = dict(value=dash.no_update, status="", help="")
    out_modal = dict(visible=dash.no_update, loading=False)
    out_others = dict(close=dash.no_update)

    # get triggered_id
    triggered_id = dash.ctx.triggered_id

    # check triggered_id
    if triggered_id == f"id-{TAG_BASE}-{TYPE}-open":
        out_name["value"] = ""
        out_desc["value"] = ""
        out_modal["visible"] = True
        return out_name, out_desc, out_modal, out_others

    # check triggered_id
    if triggered_id == f"id-{TAG}-modal-project":
        # check project name
        name = (name or "").strip()
        if len(name) < 4:
            out_name["status"] = "error"
            out_name["help"] = "project name is too short"
            return out_name, out_desc, out_modal, out_others

        # check project name
        user = app_db.session.query(User).get(user_id)
        if name in set([p.name for p in user.projects if p.status == 1]):
            out_name["status"] = "error"
            out_name["help"] = "project name already exists"
            return out_name, out_desc, out_modal, out_others

        # add new project
        _id = get_md5(name + str(time.time()))
        project = Project(id=_id, name=name, desc=(desc or "").strip())
        project_user = ProjectUser(user_id=user.id, project_id=project.id)

        # add to database
        app_db.session.add_all([project, project_user])
        app_db.session.commit()

        # update page
        out_modal["visible"] = False
        out_others["close"] = time.time()
        return out_name, out_desc, out_modal, out_others

    # return result (never reach here)
    return out_name, out_desc, out_modal, out_others
