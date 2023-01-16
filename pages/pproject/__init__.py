# _*_ coding: utf-8 _*_

"""
project page
"""

import dash
import feffery_antd_components as fac
import flask_login
from dash import Input, Output, dcc, html

from app import app_db
from models.users import User
from .. import comps

TAG = "project"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # return layout
    return fac.AntdContent(children=[
        comps.get_component_header(None, user_title, dot=True),

        html.Div(children=[
            fac.AntdRow(children=[
                fac.AntdCol(html.Span("Project List")),
                fac.AntdCol(fac.AntdButton("Add New Project", type="primary")),
            ], align="middle", justify="space-between", className=None),
            html.Div(id=f"id-{TAG}-list", className="bg-white mt-2 p-4"),
        ], className="w-75 m-auto mt-4"),

        dcc.Store(id=f"id-{TAG}-store", data=dict(user_id=current_user.id)),
    ], className="vh-100 overflow-auto bg-main")


@dash.callback([
    Output(f"id-{TAG}-list", "children"),

], [
    Input(f"id-{TAG}-store", "data"),
], prevent_initial_call=False)
def update_list(store_data):
    user = app_db.session.query(User).get(store_data["user_id"])

    if not user.projects:
        return fac.AntdEmpty(locale="en-US", description="No Project"),
    return html.Span(user.projects),
