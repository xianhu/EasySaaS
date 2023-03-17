# _*_ coding: utf-8 _*_

"""
files page
"""

import os

import feffery_antd_components as fac
from dash import html
from flask import request

from app import server

TAG_BASE = "analysis"
TAG = "analysis-files"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # return result
    return html.Div(fac.AntdUpload(buttonContent="upload", apiUrl="/upload/", multiple=True))


# upload file
@server.route("/upload/", methods=["POST"])
def _route_upload():
    _id = request.values.get("uploadId")
    filename = request.files["file"].filename

    # mkdir if not exists
    path = f"/tmp/{_id}"
    if not os.path.exists(path):
        os.mkdir(path)

    # write file to path
    chunk_size = 1024 * 1024
    with open(f"{path}/{filename}", "wb") as f:
        for chunk in iter(lambda: request.files["file"].read(chunk_size), b''):
            f.write(chunk)

    # return result
    return {"filename": filename}
