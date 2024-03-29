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
from core.settings import settings

TAG_BASE = "analysis"
TAG = "analysis-upload"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        # upload with flow.js
        html.Div(className="d-none", id=f"id-{TAG}-div-flow"),  # add input tag to this div
        fac.AntdButton("Upload File", id=f"id-{TAG}-upload-flow"),  # button to trigger upload
        fuc.FefferySessionStorage(id=f"id-{TAG}-storage-flow"),

        # params to trigger clientside callback
        dcc.Store(id=f"id-{TAG}-params-flow", data=dict(
            id_div=f"id-{TAG}-div-flow",
            id_button=f"id-{TAG}-upload-flow",
        )),

        # message to show information
        html.Div(id=f"id-{TAG}-message-flow"),
    ], className="vh-100 overflow-auto px-4 py-3")


# trigger clientside callback
dash.clientside_callback(
    ClientsideFunction(
        namespace="ns_flow",
        function_name="render_flow",
    ),
    Output(f"id-{TAG}-div-flow", "data"),
    Input(f"id-{TAG}-params-flow", "data"),
)


@dash.callback(
    Output(f"id-{TAG}-message-flow", "children"),
    Input(f"id-{TAG}-storage-flow", "data"),
    prevent_initial_call=True,
)
def _update_page(data_storage):
    content = f"upload: {data_storage}"
    return fac.AntdMessage(content=content, top=50)


@server.route("/upload", methods=["POST"])
def _route_upload():
    # verify token if needed
    # define uuid of session
    if not flask_session.get("uuid"):
        flask_session["uuid"] = str(uuid.uuid4())
    str_uuid = flask_session.get("uuid")

    # get file_name and file_target
    file_dir = settings.FOLDER_UPLOAD
    file_name = request.form.get("flowFilename")
    file_target = os.path.join(file_dir, f"{str_uuid}_{file_name}")

    # get chunk_number
    chunk_number = int(request.form.get("flowChunkNumber", 1))

    # write file to target
    file_mode = "wb" if chunk_number == 1 else "ab"
    with open(file_target, file_mode) as file_out:
        file = request.files.get("file")
        file_out.write(file.read())

    # return result
    return jsonify({"success": True})
