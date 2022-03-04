# _*_ coding: utf-8 _*_

"""
upload of page
"""

import base64

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from app import app, app_db
from config import config_dir_store

from ..paths import PATH_ANALYSIS, PATH_LOGIN

TAG = "analysis-upload"
ARGS_UP = {"accept": ".csv,.xls,.xlsx", "max_size": 1024 * 1024 * 10}


def layout(pathname, search):
    """
    layout of component
    """
    # define components
    _class = "position-static text-center"
    button = dbc.Button("Upload Data", class_name="w-75")
    upload = dcc.Upload(button, id=f"id-{TAG}-upload", **ARGS_UP, className=_class)

    # define components
    desc, href = "format description", f"{PATH_ANALYSIS}-upload-desc"
    tooltip = html.Div(html.A(desc, href=href, className="small text-muted"), className="text-center")
    address = html.A(id={"type": "id-address", "index": TAG}, className="_class_address_dummpy")

    # return result
    return html.Div([address, upload, tooltip], className="my-4")


@app.callback(Output({"type": "id-address", "index": TAG}, "href"), [
    Input(f"id-{TAG}-upload", "contents"),
    State(f"id-{TAG}-upload", "filename"),
], prevent_initial_call=True)
def _button_click(contents, filename):
    # check user
    user = flask_login.current_user
    if not user.is_authenticated:
        return PATH_LOGIN

    # store data
    content_type, content_string = contents.split(",")
    with open(f"{config_dir_store}/{user.id}-{filename}", "wb") as file_out:
        file_out.write(base64.b64decode(content_string))

        # commit user
        user.filename = filename
        app_db.session.merge(user)
        app_db.session.commit()

    # return result
    return f"{PATH_ANALYSIS}-table"
