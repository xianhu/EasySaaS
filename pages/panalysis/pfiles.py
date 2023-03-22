# _*_ coding: utf-8 _*_

"""
files page
"""

import base64
import os

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html, Input, Output, State
from flask import request

from app import server

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
    return html.Div(children=[
        # upload with fac.AntdUpload
        fac.AntdUpload(buttonContent="upload", apiUrl="/upload/"),
        # upload with dcc.Upload
        dcc.Upload(fac.AntdButton(children=[
            fac.AntdIcon(icon="antd-plus"),
            html.Span("Upload", className="ms-2"),
        ]), id=f"id-{TAG}-upload", className="mt-2"),
        fac.AntdSpin(html.Div(id=f"id-{TAG}-result", className="mt-2")),
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
    ], className="w-50")


@server.route("/upload/", methods=["POST"])
def _route_upload():
    # get variables
    _id = request.values.get("uploadId")
    filename = request.files["file"].filename

    # mkdir if not exists
    path_save = f"/tmp/{_id}"
    if not os.path.exists(path_save):
        os.mkdir(path_save)

    # write file to path
    chunk_size = 1024 * 1024
    with open(f"{path_save}/{filename}", "wb") as f:
        for chunk in iter(lambda: request.files["file"].read(chunk_size), b''):
            f.write(chunk)

    # return result
    return {"filename": filename}


@dash.callback(
    Output(f"id-{TAG}-result", "children"),
    Input(f"id-{TAG}-upload", "contents"),
    State(f"id-{TAG}-upload", "filename"),
    State(f"id-{TAG}-upload", "last_modified"),
)
def _upload_file(contents, filename, last_modified):
    if contents is None:
        return None

    # parse contents
    content_type, content_string = contents.split(",")
    content_decoded = base64.b64decode(content_string)
    with open(f"/tmp/{filename}", "wb") as file_out:
        file_out.write(content_decoded)

    # return result
    return html.Span(f"filename: {filename}, last_modified: {last_modified}")
