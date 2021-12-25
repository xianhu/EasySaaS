# _*_ coding: utf-8 _*_

"""
upload of page
"""

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from app import app
from config import config_dir_store
from utility.address import AddressAIO
from ..paths import PATH_ANALYSIS, PATH_LOGIN

TAG = "analysis-upload"
ADDRESS = AddressAIO(f"id-{TAG}-address")


def layout(pathname, search):
    """
    layout of component
    """
    # define components
    class_upload = "position-static text-center"
    button = dbc.Button("Upload Data", class_name="w-75")
    upload = dcc.Upload(button, id=f"id-{TAG}-upload", accept=".csv,.xlsx", className=class_upload)

    # define components
    desc, href = "format description", f"{PATH_ANALYSIS}-upload-desc"
    tooltip = html.Div(html.A(desc, href=href, className="small text-muted"), className="text-center")

    # return result
    return html.Div([ADDRESS, upload, tooltip], className="my-4")


@app.callback(Output(f"id-{TAG}-address", "href"), [
    Input(f"id-{TAG}-upload", "filename"),
    State(f"id-{TAG}-upload", "contents"),
], prevent_initial_call=True)
def _button_click(filename, contents):
    user = flask_login.current_user
    if not user.is_authenticated:
        return PATH_LOGIN
    with open(f"{config_dir_store}/{user.id}-{filename}", "w") as file_in:
        file_in.write(contents)
    return f"{PATH_ANALYSIS}-table"
