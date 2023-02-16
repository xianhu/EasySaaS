# _*_ coding: utf-8 _*_

"""
projects page
"""

import dash
import feffery_antd_components as fac
import flask_login
from dash import Input, Output, State, dcc, html

from app import app_db
from models.users import User
from utility.paths import PATH_ANALYSIS
from . import pnewp
from ..comps import header as comps_header

TAG = "projects"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # define components
    modal_newp = pnewp.layout(pathname, search)
    data_newp = dcc.Store(id=f"id-{TAG}-data-newp", data=0)

    # define components
    button_new = fac.AntdButton("Add New Project", id=f"id-{TAG}-button-new", type="primary")
    col_list = [fac.AntdCol(html.Span("Project List")), fac.AntdCol(button_new)]

    # return result
    data_uid = dcc.Store(id=f"id-{TAG}-data-uid", data=current_user.id)
    return html.Div(children=[
        comps_header.get_component_header(user_title=user_title, dot=True),
        html.Div(children=[
            fac.AntdRow(col_list, align="bottom", justify="space-between"),
            html.Div(id=f"id-{TAG}-div-main", className="bg-white mt-2 p-4"),
        ], className="w-75 m-auto mt-4"),
        modal_newp, data_newp, data_uid,
    ], className="bg-main vh-100 overflow-auto")


@dash.callback([
    Output(f"id-{TAG}-div-main", "children"),
    Output(f"id-{TAG}-button-new", "disabled"),
], [
    Input(f"id-{TAG}-data-newp", "data"),
    State(f"id-{TAG}-data-uid", "data"),
], prevent_initial_call=False)
def _update_page(_newp_data, user_id):
    user = app_db.session.query(User).get(user_id)
    projects_list = [p for p in user.projects if p.status == 1]

    # check projects
    if not projects_list:
        return fac.AntdEmpty(description="No Project"), False

    # define components
    div_list = [fac.AntdRow(children=[
        fac.AntdCol(html.Span("Project Name", className="fw-bold"), span=6),
        fac.AntdCol(html.Span("Project Description", className="fw-bold"), span=10),
        fac.AntdCol(html.Span("Project Status", className="fw-bold"), span=4),
        fac.AntdCol(html.Span("Operation", className="fw-bold"), span=4),
    ]), fac.AntdDivider(className="my-3")]

    # define components
    for project in projects_list:
        href = f"{PATH_ANALYSIS}?project_id={project.id}"
        div_list.append(fac.AntdRow(children=[
            fac.AntdCol(html.Span(project.name), span=6),
            fac.AntdCol(html.Span(project.desc), span=10),
            fac.AntdCol(html.Span(project.status), span=4),
            fac.AntdCol(html.A("Detail", href=href), span=4),
        ]))
        div_list.append(fac.AntdDivider(className="my-3"))

    # return result
    return div_list, False if len(projects_list) < 3 else True
