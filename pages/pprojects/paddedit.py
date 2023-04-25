# _*_ coding: utf-8 _*_

"""
add/edit project
"""

import time

import dash
import feffery_antd_components as fac
from dash import Input, Output, State

from models import DbMaker
from models.crud import crud_project
from models.schemas import ProjectCreate, ProjectUpdate

TAG_BASE = "projects"
TAG = "projects-addedit"

# type of page
TYPE = "addedit"


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
    form_items = fac.AntdForm(children=[form_name, form_desc], layout="vertical")

    # return result
    return fac.AntdModal(form_items, id=f"id-{TAG}-modal-project", **dict(
        title="Add/Edit", visible=False, closable=False, maskClosable=False,
        okText="Confirm", cancelText="Cancel", okClickClose=False,
        renderFooter=True, confirmAutoSpin=True,
    ))


@dash.callback([dict(
    value=Output(f"id-{TAG}-input-name", "value"),
    readonly=Output(f"id-{TAG}-input-name", "readOnly"),
    status=Output(f"id-{TAG}-form-name", "validateStatus"),
    help=Output(f"id-{TAG}-form-name", "help"),
), dict(
    value=Output(f"id-{TAG}-input-desc", "value"),
    readonly=Output(f"id-{TAG}-input-desc", "readOnly"),
    status=Output(f"id-{TAG}-form-desc", "validateStatus"),
    help=Output(f"id-{TAG}-form-desc", "help"),
), dict(
    visible=Output(f"id-{TAG}-modal-project", "visible"),
    loading=Output(f"id-{TAG}-modal-project", "confirmLoading"),
    title=Output(f"id-{TAG}-modal-project", "title"),
), Output(f"id-{TAG_BASE}-{TYPE}-close", "data")], [
    Input(f"id-{TAG_BASE}-{TYPE}-open", "data"),
    Input(f"id-{TAG}-modal-project", "okCounts"),
], [
    State(f"id-{TAG}-input-name", "value"),
    State(f"id-{TAG}-input-desc", "value"),
    State(f"id-{TAG_BASE}-{TYPE}-project", "data"),
], prevent_initial_call=True)
def _update_page(open_data, ok_counts, name, desc, project):
    # define outputs
    out_name = dict(value=dash.no_update, readonly=dash.no_update, status="", help="")
    out_desc = dict(value=dash.no_update, readonly=dash.no_update, status="", help="")
    out_modal = dict(visible=dash.no_update, loading=False, title=dash.no_update)

    # get triggered_id
    triggered_id = dash.ctx.triggered_id

    # check triggered_id
    if triggered_id == f"id-{TAG_BASE}-{TYPE}-open":
        is_add = not project.get("id")

        # update name and desc
        out_name["value"] = "" if is_add else project["name"]
        out_name["readonly"] = False if is_add else True
        out_desc["value"] = "" if is_add else project["desc"]
        out_desc["readonly"] = False if is_add else False

        # update modal title
        out_modal["title"] = f"{'Add' if is_add else 'Edit'} Project"

        # update modal and return
        out_modal["visible"] = True
        return out_name, out_desc, out_modal, dash.no_update

    # check triggered_id
    if triggered_id == f"id-{TAG}-modal-project":
        # check project name
        name = (name or "").strip()
        if len(name) < 6:
            out_name["status"] = "error"
            out_name["help"] = "project name is too short"
            return out_name, out_desc, out_modal, dash.no_update
        desc = (desc or "").strip()

        # check project id
        if not project.get("id"):
            # create project
            with DbMaker() as db:
                user_id = project["user_id"]
                project_schema = ProjectCreate(name=name, desc=desc, user_id=user_id)
                crud_project.create(db, obj_schema=project_schema)
        else:
            # update project
            with DbMaker() as db:
                project_db = crud_project.get(db, _id=project["id"])
                project_schema = ProjectUpdate(desc=desc)
                crud_project.update(db, obj_db=project_db, obj_schema=project_schema)

        # update modal and return
        out_modal["visible"] = False
        return out_name, out_desc, out_modal, time.time()

    # return result (never reach here)
    return out_name, out_desc, out_modal, dash.no_update
