# _*_ coding: utf-8 _*_

"""
upload page
"""

import base64
import os
import uuid

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html, Input, Output, State, ClientsideFunction
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

    # define uuid to session
    # flask_session["uuid"] = str(uuid.uuid4())

    # return result
    return html.Div(children=[
        # upload with dcc.Upload
        dcc.Upload(fac.AntdButton(children_button), id=f"id-{TAG}-upload"),
        html.Div(id=f"id-{TAG}-result", className="mt-2 mb-3"),

        # upload with flow.js
        fac.AntdButton(children_button, id=f"id-{TAG}-upload-flow"),
        html.Div(id=f"id-{TAG}-result-flow", className="mt-2"),

        # upload with flow.js <input and js>
        html.Div(id=f"id-{TAG}-div-flow", className="d-none"),
        fuc.FefferySessionStorage(id=f"id-key-flow"),
        dcc.Store(id=f"id-{TAG}-store-flow", data={
            "id_div": f"id-{TAG}-div-flow",
            "id_button": f"id-{TAG}-upload-flow",
        }),
        # fuc.FefferyExecuteJs(jsString=get_js_flow(
        #     id_div=f"id-{TAG}-div-flow",
        #     id_button=f"id-{TAG}-upload-flow",
        #     id_storage=f"id-{TAG}-storage-flow",
        # )),

        # define style
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
    ], className=None)


dash.clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="render_flow",
    ),
    Output(f"id-{TAG}-div-flow", "children"),
    Input(f"id-{TAG}-store-flow", "data"),
    prevent_initial_call=False,
)


@dash.callback(
    Output(f"id-{TAG}-result", "children"),
    Input(f"id-{TAG}-upload", "contents"),
    State(f"id-{TAG}-upload", "filename"),
    State(f"id-{TAG}-upload", "last_modified"),
)
def _upload_file(contents, file_name, last_modified):
    if contents is None:
        return None

    # get target_file
    str_uuid = flask_session.get("uuid", "")
    target_file = os.path.join("/tmp", f"{str_uuid}_{file_name}")

    # parse contents
    content_type, content_string = contents.split(",")
    content_decoded = base64.b64decode(content_string)

    # write file to target
    with open(target_file, "wb") as file_out:
        file_out.write(content_decoded)

    # return result
    return html.Span(f"file_name: {file_name}, last_modified: {last_modified}")


@server.route("/upload", methods=["POST"])
def _route_upload():
    # get file_name and target_file
    str_uuid = flask_session.get("uuid", "")
    file_name = request.form.get("flowFilename")
    target_file = os.path.join("/tmp", f"{str_uuid}_{file_name}")

    # calculate file_mode based on chunk_number
    chunk_number = int(request.form.get("flowChunkNumber", 1))
    file_mode = "wb" if chunk_number == 1 else "ab"

    # write file to target
    with open(target_file, file_mode) as file_out:
        file = request.files.get("file")
        file_out.write(file.read())

    # return result
    return jsonify({"success": True})


@dash.callback(
    Output(f"id-{TAG}-result-flow", "children"),
    Input(f"id-key-flow", "data"),
)
def _upload_file_flow(data_storage):
    if data_storage is None:
        return None
    print(flask_session)

    # return result
    if not flask_session.get("uuid"):
        flask_session["uuid"] = str(uuid.uuid4())
    return html.Span(str(data_storage))
