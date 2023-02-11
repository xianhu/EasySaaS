# _*_ coding: utf-8 _*_

"""
project page
"""

import dash
import feffery_antd_components as fac
import flask_login
from dash import Input, Output, State, dcc, html

from app import app_db
from models.users import User
from . import pnewp
from ..comps import header as comps_header

TAG = "project"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user

    # define variables
    user_id = current_user.id
    user_title = current_user.email.split("@")[0]

    # define components
    header_page = comps_header.get_component_header(None, user_title, dot=True)

    # define components
    button_new = fac.AntdButton("Add New Project", id=f"id-{TAG}-button-new", type="primary")
    col_list = [fac.AntdCol(html.Span("Project List")), fac.AntdCol(button_new)]
    row_header = fac.AntdRow(col_list, align="middle", justify="space-between")

    # define components
    div_list = html.Div(id=f"id-{TAG}-div-list", className="bg-white mt-2 p-4")
    div_main = html.Div([row_header, div_list], className="w-75 m-auto mt-4")

    # define components
    modal_newp = pnewp.layout(pathname, search, user_id=user_id)

    # define components
    data_uid = dcc.Store(id=f"id-{TAG}-data-uid", data=user_id)
    data_newp = dcc.Store(id=f"id-{TAG}-data-newp", data=0)

    # return result
    class_div = "bg-main vh-100 overflow-auto"
    return html.Div([header_page, div_main, modal_newp, data_uid, data_newp], className=class_div)


@dash.callback([
    Output(f"id-{TAG}-div-list", "children"),
    Output(f"id-{TAG}-button-new", "disabled"),
], [
    Input(f"id-{TAG}-data-newp", "data"),
    State(f"id-{TAG}-data-uid", "data"),
], prevent_initial_call=False)
def _update_content(_, user_id):
    user = app_db.session.query(User).get(user_id)
    if not user.projects:
        return fac.AntdEmpty(locale="en-US", description="No Project"), False
    return html.Span(", ".join([p.name for p in user.projects])), False
