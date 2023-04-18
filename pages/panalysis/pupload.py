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
STYLE_PAGE = ""


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        # upload with flow.js
        html.Div(className="d-none", id=f"id-{TAG}-div-upload"),
        fac.AntdButton("Upload File", id=f"id-{TAG}-button-upload"),
        fuc.FefferySessionStorage(id=f"id-{TAG}-storage-upload"),

        # params to trigger clientside callback
        dcc.Store(id=f"id-{TAG}-params-upload", data=dict(
            id_div=f"id-{TAG}-div-upload",
            id_button=f"id-{TAG}-button-upload",
        )),

        # define message and style
        html.Div(id=f"id-{TAG}-message-upload"),
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
    ], className="vh-100 overflow-auto px-4 py-3")


# trigger clientside callback
dash.clientside_callback(
    ClientsideFunction(
        namespace="ns_flow",
        function_name="render_flow",
    ),
    Output(f"id-{TAG}-div-upload", "data"),
    Input(f"id-{TAG}-params-upload", "data"),
)


@dash.callback(
    Output(f"id-{TAG}-message-upload", "children"),
    Input(f"id-{TAG}-storage-upload", "data"),
    prevent_initial_call=True,
)
def _update_page(data_storage):
    content = f"upload: {data_storage}"
    return fac.AntdMessage(content=content, top=50)


@server.route("/upload", methods=["POST"])
def _route_upload():
    # define uuid of session
    if not flask_session.get("uuid"):
        flask_session["uuid"] = str(uuid.uuid4())
    str_uuid = flask_session.get("uuid")

    # get file_name and file_target
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
