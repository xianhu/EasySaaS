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
from models.users import User
from utility.paths import PATH_ANALYSIS
from . import paddp, peditp, pdelp
from ..comps import header as comps_header

TAG = "projects"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # define components for add project
    modal_addp = paddp.layout(pathname, search)
    data_addp_open = dcc.Store(id=f"id-{TAG}-addp-open", data=0)
    data_addp_close = dcc.Store(id=f"id-{TAG}-addp-close", data=0)
    data_addp_pid = dcc.Store(id=f"id-{TAG}-addp-pid", data=None)

    # define components for edit project
    modal_editp = peditp.layout(pathname, search)
    data_editp_open = dcc.Store(id=f"id-{TAG}-editp-open", data=0)
    data_editp_close = dcc.Store(id=f"id-{TAG}-editp-close", data=0)
    data_editp_pid = dcc.Store(id=f"id-{TAG}-editp-pid", data=None)

    # define components for delete project
    modal_delp = pdelp.layout(pathname, search)
    data_delp_open = dcc.Store(id=f"id-{TAG}-delp-open", data=0)
    data_delp_close = dcc.Store(id=f"id-{TAG}-delp-close", data=0)
    data_delp_pid = dcc.Store(id=f"id-{TAG}-delp-pid", data=None)

    # define components
    button_add = fac.AntdButton("Add New Project", id=f"id-{TAG}-button-new", href=f"#add", type="primary")
    col_list = [fac.AntdCol(html.Span("Project List")), fac.AntdCol(button_add, className=None)]

    # return result
    return html.Div(children=[
        # define components
        comps_header.get_component_header(user_title=user_title, dot=True),
        html.Div(children=[
            fac.AntdRow(col_list, align="bottom", justify="space-between"),
            html.Div(id=f"id-{TAG}-div-main", className="bg-white mt-2 p-4"),
        ], className="w-75 m-auto mt-4"),
        # define components of modal
        modal_addp, data_addp_open, data_addp_close, data_addp_pid,
        modal_editp, data_editp_open, data_editp_close, data_editp_pid,
        modal_delp, data_delp_open, data_delp_close, data_delp_pid,
        # define components of others
        dcc.Location(id=f"id-{TAG}-location-current", refresh=False),
        dcc.Store(id=f"id-{TAG}-data-uid", data=current_user.id),
    ], className="bg-main vh-100 overflow-auto")


@dash.callback([
    Output(f"id-{TAG}-button-new", "disabled"),
    Output(f"id-{TAG}-div-main", "children"),
], [
    Input(f"id-{TAG}-addp-close", "data"),
    Input(f"id-{TAG}-editp-close", "data"),
    Input(f"id-{TAG}-delp-close", "data"),
    State(f"id-{TAG}-data-uid", "data"),
], prevent_initial_call=False)
def _update_page(_add, _edit, _del, user_id):
    # get user and projects
    user = app_db.session.query(User).get(user_id)
    projects_list = [p for p in user.projects if p.status == 1]

    # check projects
    if not projects_list:
        return False, fac.AntdEmpty(description="No Project")

    # define components
    div_list = [fac.AntdRow(children=[
        fac.AntdCol(html.Span("Project Name", className="fw-bold"), span=5),
        fac.AntdCol(html.Span("Project Description", className="fw-bold"), span=12),
        fac.AntdCol(html.Span("Project Status", className="fw-bold"), span=2),
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
                html.A("Delete", href=f"#del#{project.id}", className="ms-3 text-danger"),
            ], span=5),
        ]))
        div_list.append(fac.AntdDivider(className="my-3"))

    # return result
    return False if len(projects_list) < 3 else True, div_list


@dash.callback([dict(
    open=Output(f"id-{TAG}-addp-open", "data"),
    pid=Output(f"id-{TAG}-addp-pid", "data"),
), dict(
    open=Output(f"id-{TAG}-editp-open", "data"),
    pid=Output(f"id-{TAG}-editp-pid", "data"),
), dict(
    open=Output(f"id-{TAG}-delp-open", "data"),
    pid=Output(f"id-{TAG}-delp-pid", "data"),
), dict(
    vhash=Output(f"id-{TAG}-location-current", "hash"),
)], [
    Input(f"id-{TAG}-location-current", "hash"),
], prevent_initial_call=True)
def _update_page(vhash):
    # define outputs
    out_addp = dict(open=dash.no_update, pid=None)
    out_editp = dict(open=dash.no_update, pid=None)
    out_delp = dict(open=dash.no_update, pid=None)
    out_others = dict(vhash="")

    # get fragments of vhash
    frags = vhash.lstrip("#").split("#")

    # check hash for add
    if len(frags) >= 1 and frags[0] == "add":
        out_addp["open"] = time.time()
        # out_addp["pid"] = None
        return out_addp, out_editp, out_delp, out_others

    # check hash for edit
    if len(frags) >= 2 and frags[0] == "edit":
        out_editp["open"] = time.time()
        out_editp["pid"] = frags[1]
        return out_addp, out_editp, out_delp, out_others

    # check hash for delete
    if len(frags) >= 2 and frags[0] == "del":
        out_delp["open"] = time.time()
        out_delp["pid"] = frags[1]
        return out_addp, out_editp, out_delp, out_others

    # return result
    return out_addp, out_editp, out_delp, out_others
