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

TAG_BASE = "analysis"
TAG = "analysis-files"

# style of page
STYLE_PAGE = """
    .ant-btn, .ant-btn > span {
        display: flex !important;
        align-items: center !important;
    }
"""


def _get_js_flow(id_div_input, id_button_upload, id_output):
    """
    get js according to flow.js
    """
    return f"""
        // add input to div
        var div = document.getElementById('{id_div_input}');
        div.innerHTML="<input id='id-input-file' type='file' name='file' style='display:none;'/>";

        // bind button click event to input
        document.getElementById('{id_button_upload}').addEventListener('click', function() {{
            document.getElementById('id-input-file').click();
        }});
        
        // define flow instance
        var flow = new Flow({{
            target: '/upload',
            testChunks: false,
            uploadMethod: 'POST',
            chunkSize: 1024 * 1024,
            simultaneousUploads: 1,          
        }});
        
        // define flow events
        flow.on('fileAdded', function (file, event) {{ console.log('file added'); }});
        flow.on('fileSuccess', function (file, message) {{ console.log('file success'); }});
        flow.on('fileError', function (file, message) {{ console.log('file error'); }});

        // define output component for progress
        var output = document.getElementById('{id_output}');
        flow.on('fileProgress', function (file) {{
            let percent = Math.floor(file.progress() * 100);
            output.innerHTML = 'progress: ' + percent + '%';
        }});

        // bind input change event to flow
        document.getElementById('id-input-file').addEventListener('change', function(event) {{
            flow.addFile(event.target.files[0]);
            flow.upload();
        }});
    """


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    children_button = [
        fac.AntdIcon(icon="antd-plus"),
        html.Span("Upload", className="ms-1"),
    ]

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
        fuc.FefferyExecuteJs(jsString=_get_js_flow(
            id_div_input=f"id-{TAG}-div-flow",
            id_button_upload=f"id-{TAG}-upload-flow",
            id_output=f"id-{TAG}-result-flow",
        )),

        # define style
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
    ], className="w-50")


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


@server.route("/upload", methods=["POST"])
def _route_upload():
    # get parameters
    file_name = request.form.get("flowFilename")
    target_file = os.path.join("/tmp", file_name)
    chunk_number = int(request.form.get("flowChunkNumber", 1))

    # write file to target
    if chunk_number == 1:
        with open(target_file, "wb") as file_out:
            file_out.write(b"")
    with open(target_file, "ab") as file_out:
        file = request.files.get("file")
        file_out.write(file.read())

    # return result
    return flask.jsonify({"success": True})
