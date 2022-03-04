# _*_ coding: utf-8 _*_

"""
Layout
"""

import logging

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, MATCH, dcc, html

from app import app, server
from config import config_app_name
from pages import palert, pintros
from pages import panalysis, psign, puser
from pages.paths import *

# app layout
app.title = config_app_name
app.layout = html.Div(children=[
    html.Div(id="id-content", className=None),
    dcc.Location(id="id-location", refresh=False),
    dcc.Store(id="id-session", storage_type="session"),
    dcc.Store(id="id-stodata", storage_type="session"),
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
    pathname = PATH_INTROS if pathname == "/" else pathname
    store_data = {"title": pathname.strip("/")}

    # =====================================================
    if pathname == PATH_INTROS:
        return pathname, pintros.layout(pathname, search)

    # =====================================================
    if pathname == PATH_LOGIN:
        if flask_login.current_user.is_authenticated:
            return PATH_ANALYSIS, panalysis.layout(PATH_ANALYSIS, search)
        return pathname, psign.layout(pathname, search)

    if pathname == PATH_LOGOUT:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, psign.layout(pathname, search)

    # =====================================================
    if pathname.startswith(PATH_REGISTERE):
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, psign.layout(pathname, search)

    if pathname.startswith(PATH_RESETPWDE):
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, psign.layout(pathname, search)

    # =====================================================
    if pathname.startswith(PATH_USER):
        if not flask_login.current_user.is_authenticated:
            return PATH_LOGIN, psign.layout(PATH_LOGIN, search)
        return pathname, puser.layout(pathname, search)

    # =====================================================
    if pathname.startswith(PATH_ANALYSIS):
        if not flask_login.current_user.is_authenticated:
            return PATH_LOGIN, psign.layout(PATH_LOGIN, search)
        return pathname, panalysis.layout(pathname, search)

    # return 404 ==========================================
    return pathname, palert.layout_404(pathname, search, return_href=PATH_INTROS)


# clientside callback
app.clientside_callback(
    """
    function(href) {
        if (href != null && href != undefined) {
            window.location.href = href
        }
        return href
    }
    """,
    Output({"type": "id-address", "index": MATCH}, "data"),
    Input({"type": "id-address", "index": MATCH}, "href"),
    prevent_initial_call=True,
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8088, debug=True)
