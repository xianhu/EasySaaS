# _*_ coding: utf-8 _*_

"""
files page
"""

import base64
import os

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
import flask
from dash import dcc, html, Input, Output, State
from flask import request

from app import server
from .funcs import get_js_flow

TAG_BASE = "analysis"
TAG = "analysis-files"

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
        # upload with dcc.Upload
        dcc.Upload(fac.AntdButton(children_button), id=f"id-{TAG}-upload"),
        html.Div(id=f"id-{TAG}-result", className="mt-2 mb-3"),

        # upload with flow.js
        fac.AntdButton(children_button, id=f"id-{TAG}-upload-flow"),
        html.Div(id=f"id-{TAG}-result-flow", className="mt-2"),

        # upload with flow.js <input and js>
        html.Div(id=f"id-{TAG}-div-flow", className="d-none"),
        fuc.FefferySessionStorage(id=f"id-{TAG}-status-flow"),
        fuc.FefferyExecuteJs(jsString=get_js_flow(
            id_div_input=f"id-{TAG}-div-flow",
            id_button_upload=f"id-{TAG}-upload-flow",
            id_storage=f"id-{TAG}-status-flow",
        )),

        # define style
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
    ], className=None)


@dash.callback(
    Output(f"id-{TAG}-result", "children"),
    Input(f"id-{TAG}-upload", "contents"),
    State(f"id-{TAG}-upload", "filename"),
    State(f"id-{TAG}-upload", "last_modified"),
)
def _upload_file(contents, filename, last_modified):
    if contents is None:
        return None
    target_file = os.path.join("/tmp", filename)

    # parse contents
    content_type, content_string = contents.split(",")
    content_decoded = base64.b64decode(content_string)

    # write file to target
    with open(target_file, "wb") as file_out:
        file_out.write(content_decoded)

    # return result
    return html.Span(f"filename: {filename}, last_modified: {last_modified}")


@dash.callback(
    Output(f"id-{TAG}-result-flow", "children"),
    Input(f"id-{TAG}-status-flow", "data"),
)
def _upload_file_flow(data):
    if data is None:
        return None
    return html.Span(f"status: {data}")


@server.route("/upload", methods=["POST"])
def _route_upload():
    # get parameters
    file_name = request.form.get("flowFilename")
    target_file = os.path.join("/tmp", file_name)
    chunk_number = int(request.form.get("flowChunkNumber", 1))

    # write file to target
    file = request.files.get("file")
    file_mode = "wb" if chunk_number == 1 else "ab"
    with open(target_file, file_mode) as file_out:
        file_out.write(file.read())

    # return result
    return flask.jsonify({"success": True})
