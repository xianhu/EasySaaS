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
from ..comps import header as comps_header

TAG = "project"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user

    # define components
    user_title = current_user.email.split("@")[0]
    header = comps_header.get_component_header(None, user_title, dot=True)

    # define components
    button_new = fac.AntdButton("Add New Project", id=f"id-{TAG}-new", type="primary")
    col_list = [fac.AntdCol(html.Span("Project List")), fac.AntdCol(button_new)]
    row_header = fac.AntdRow(col_list, align="middle", justify="space-between")

    # define components
    div_list = html.Div(id=f"id-{TAG}-list", className="bg-white mt-2 p-4")
    div_main = html.Div([row_header, div_list], className="w-75 m-auto mt-4")

    # define components
    input_name = fac.AntdInput(id=f"id-{TAG}-input-name", placeholder="Email", size="large")
    form_name = fac.AntdFormItem(email_input, id=f"id-{TAG}-email-form", required=True)


    form_project = fac.AntdForm(children=[
        fac.AntdFormItem(fac.AntdInput(), label="project name:"),
        fac.AntdFormItem(fac.AntdInput(), label="project description:"),
    ], layout="vertical")
    div_modal = fac.AntdModal(
        form_project,
        id=f"id-{TAG}-modal", bodyStyle={},
        visible=False, closable=False, maskClosable=False,
        okText="Add New Project", okClickClose=False, okButtonProps=dict(autoSpin=True, type="danger"),
        cancelText="Cancel", renderFooter=True,
        title=html.Span("Add New Project"),
    )

    # define store data
    store_data = dcc.Store(id=f"id-{TAG}-store", data=dict(user_id=current_user.id))
    main_list = [header, div_main, store_data, div_modal]

    # return result
    return html.Div(main_list, className="vh-100 overflow-auto bg-main")


@dash.callback(
    Output(f"id-{TAG}-modal", "visible"),
    Input(f"id-{TAG}-new", "nClicks"),
    prevent_initial_call=False,
)
def add_new_project(n_clicks):
    return True


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
