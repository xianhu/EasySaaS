# _*_ coding: utf-8 _*_

"""
delete project
"""

import time

import dash
import feffery_antd_components as fac
from dash import Input, Output, State, html

from app import app_db
from models.users import Project, UserProject

TAG_BASE = "projects"
TAG = "projects-delete"
TYPE = "delete"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    span_name = html.Span(id=f"id-{TAG}-span-name", className="fw-bold")
    content = html.Div(["Are you sure to delete project: ", span_name, "?"])

    # define components
    kwargs_modal = dict(
        title="Delete Project", visible=False, closable=False, maskClosable=False,
        okText="Confirm", cancelText="Cancel", okClickClose=False,
        renderFooter=True, confirmAutoSpin=True, okButtonProps=dict(danger=True),
    )

    # return result
    return fac.AntdModal(content, id=f"id-{TAG}-modal-project", **kwargs_modal)


@dash.callback([dict(
    children=Output(f"id-{TAG}-span-name", "children"),
), dict(
    visible=Output(f"id-{TAG}-modal-project", "visible"),
    loading=Output(f"id-{TAG}-modal-project", "confirmLoading"),
), Output(f"id-{TAG_BASE}-{TYPE}-close", "data")], [
    Input(f"id-{TAG_BASE}-{TYPE}-open", "data"),
    Input(f"id-{TAG}-modal-project", "okCounts"),
    State(f"id-{TAG_BASE}-{TYPE}-project", "data"),
], prevent_initial_call=True)
def _update_page(open_data, ok_counts, project):
    # define outputs
    out_name = dict(children=dash.no_update)
    out_modal = dict(visible=dash.no_update, loading=False)

    # get triggered_id
    triggered_id = dash.ctx.triggered_id

    # check triggered_id
    if triggered_id == f"id-{TAG_BASE}-{TYPE}-open":
        out_name["children"] = project["name"]
        out_modal["visible"] = True
        return out_name, out_modal, dash.no_update

    # check triggered_id
    if triggered_id == f"id-{TAG}-modal-project":
        # delete user_project (all users)
        app_db.session.query(UserProject).filter(
            UserProject.project_id == project["id"],
        ).delete()

        # delete project (set status to 0)
        app_db.session.query(Project).filter(
            Project.id == project["id"],
        ).update({Project.status: 0})

        # commit to database
        app_db.session.commit()

        # update page
        out_modal["visible"] = False
        return out_name, out_modal, time.time()

    # return result (never reach here)
    return out_name, out_modal, dash.no_update
