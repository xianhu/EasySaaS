# _*_ coding: utf-8 _*_

"""
Layout
"""

import logging

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from app import app, server
from config import config_app_name
from pages import palert, pintros
from pages.paths import *

# app layout
app.title = config_app_name
app.layout = html.Div(children=[
    dcc.Location(id="id-location", refresh=False),
    dcc.Store(id="id-session", storage_type="session"),
    html.Div(id="id-content", className="bg-light min-vh-100"),
])

# complete layout
app.validation_layout = dbc.Container([])


@app.callback([
    Output("id-location", "pathname"),
    Output("id-content", "children"),
], [
    Input("id-location", "pathname"),
    State("id-location", "search"),
    State("id-session", "data"),
], prevent_initial_call=False)
def _init_page(pathname, search, session):
    logging.warning("pathname=%s, search=%s, session=%s", pathname, search, session)
    search = (search or "").strip("?")
    if pathname == "/":
        pathname = PATH_INTROS

    # =====================================================
    if pathname == PATH_INTROS:
        return pathname, pintros.layout(pathname, search)

    # return 404 ==========================================
    return pathname, palert.layout_404(pathname, search, PATH_INTROS)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8088, debug=True)
