# _*_ coding: utf-8 _*_

"""
files page
"""

import os

import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import html
from flask import request

from app import server

TAG_BASE = "analysis"
TAG = "analysis-files"

# define style
STYLE_PAGE = """
    .ant-btn {
        display: flex !important;
        align-items: center !important;
    }
"""


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return html.Div(children=[
        fuc.FefferyStyle(rawStyle=STYLE_PAGE),
        fac.AntdUpload(buttonContent="upload", apiUrl="/upload/"),
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
