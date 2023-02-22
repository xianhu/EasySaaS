# _*_ coding: utf-8 _*_

"""
delete project
"""

import time

import dash
import feffery_antd_components as fac
from dash import Input, Output, State, html

from app import app_db
from models.users import Project

TAG_BASE = "projects"
TAG = "projects-delp"
TYPE = "delp"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    span_name = html.Span(id=f"id-{TAG}-span-name", className="fw-bold")
    content = html.Div(["Are you sure to delete project: ", span_name, "?"])

    # define components
    kwargs_modal = dict(
        title="Delete Project", visible=False, closable=False, renderFooter=True,
        okText="Delete Project", cancelText="Cancel", okClickClose=False, confirmAutoSpin=True,
        okButtonProps=dict(danger=True),
    )

    # return result
    return fac.AntdModal(content, id=f"id-{TAG}-modal-project", **kwargs_modal)


@dash.callback([dict(
    children=Output(f"id-{TAG}-span-name", "children"),
), dict(
    visible=Output(f"id-{TAG}-modal-project", "visible"),
    loading=Output(f"id-{TAG}-modal-project", "confirmLoading"),
), dict(
    close=Output(f"id-{TAG_BASE}-{TYPE}-close", "data"),
)], [
    Input(f"id-{TAG_BASE}-{TYPE}-open", "data"),
    Input(f"id-{TAG}-modal-project", "okCounts"),
], [
    State(f"id-{TAG_BASE}-{TYPE}-pid", "data"),
    State(f"id-{TAG_BASE}-data-uid", "data"),
], prevent_initial_call=True)
def _update_page(_open_data, _ok_counts, project_id, user_id):
    # define outputs
    out_name = dict(children=dash.no_update)
    out_modal = dict(visible=dash.no_update, loading=False)
    out_others = dict(close=dash.no_update)

    # get user and project instances
    # user = app_db.session.query(User).get(user_id)
    project = app_db.session.query(Project).get(project_id)

    # get trigger_id
    trigger_id = dash.ctx.triggered_id

    # check trigger_id
    if trigger_id == f"id-{TAG_BASE}-{TYPE}-open":
        out_name["children"] = project.name
        out_modal["visible"] = True
        return out_name, out_modal, out_others

    # check trigger_id
    if trigger_id == f"id-{TAG}-modal-project":
        # delete project
        project.status = 0
        app_db.session.commit()

        # update page
        out_modal["visible"] = False
        out_others["close"] = time.time()
        return out_name, out_modal, out_others

    # return result (never reach here)
    return out_name, out_modal, out_others
