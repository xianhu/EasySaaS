# _*_ coding: utf-8 _*_

"""
upload page
"""

import os
import uuid

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import ClientsideFunction, Input, Output, dcc, html
from flask import jsonify, request
from flask import session as flask_session

from app import server

TAG_BASE = "analysis"
TAG = "analysis-upload"

# style of page
STYLE_PAGE = """
    .ant-btn, .ant-btn > span {
        display: flex !important;
        align-items: center !important;
    }
"""


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    icon_plus = fac.AntdIcon(icon="antd-plus")
    span_upload = html.Span("Upload", className="ms-1")
    children_button = [icon_plus, span_upload]

    # return result
    return html.Div(children=[
        # upload with flow.js <button and result>
        fac.AntdButton(children_button, id=f"id-{TAG}-upload-flow"),
        html.Div(id=f"id-{TAG}-result-flow", className="mt-2"),

        # upload with flow.js <input and storage>
        html.Div(id=f"id-{TAG}-div-flow", className="d-none"),
        dcc.Store(id=f"id-{TAG}-params-flow", data=dict(
            id_div=f"id-{TAG}-div-flow",
            id_button=f"id-{TAG}-upload-flow",
        )),
        fuc.FefferySessionStorage(id="id-storage-flow"),

        # define style of this page
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
    ], className=None)


# trigger clientside callback
dash.clientside_callback(
    ClientsideFunction(
        namespace="ns_flow",
        function_name="render_flow",
    ),
    Output(f"id-{TAG}-div-flow", "data"),
    Input(f"id-{TAG}-params-flow", "data"),
    prevent_initial_call=True,
)


@dash.callback(
    Output(f"id-{TAG}-result-flow", "children"),
    Input(f"id-storage-flow", "data"),
    prevent_initial_call=True,
)
def _update_page(data_storage):
    if data_storage is None:
        return None
    return html.Span(str(data_storage))


@server.route("/upload", methods=["POST"])
def _route_upload():
    # define uuid of session
    if not flask_session.get("uuid"):
        flask_session["uuid"] = str(uuid.uuid4())
    str_uuid = flask_session.get("uuid")

    # get file_name and target_file
    file_name = request.form.get("flowFilename")
    file_target = os.path.join("/tmp", f"{str_uuid}_{file_name}")

    # get chunk_number
    chunk_number = int(request.form.get("flowChunkNumber", 1))

    # write file to target
    file_mode = "wb" if chunk_number == 1 else "ab"
    with open(file_target, file_mode) as file_out:
        file = request.files.get("file")
        file_out.write(file.read())

    # return result
    return jsonify({"success": True})
