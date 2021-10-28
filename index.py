# _*_ coding: utf-8 _*_

"""
Layout
"""

import logging

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc

from app import app, server
from config import config_app_name
from pages import pcommon, pindex, pmine, psystem
from pages.consts import *
from pages.pcommon import palert

# app layout
app.title = config_app_name
app.layout = dbc.Container(children=[
    dcc.Location(id="id-location", refresh=False),
    dcc.Store(id="id-session", storage_type="session"),
    dbc.Container(id="id-content", class_name="vh-100"),
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
    search = (search or "").strip("?")
    logging.warning("pathname=%s, search=%s, session=%s", pathname, search, session)

    # =====================================================
    if pathname == PATH_LOGIN:
        if flask_login.current_user.is_authenticated:
            return PATH_SYSTEM, psystem.layout(PATH_SYSTEM, search)
        return pathname, pcommon.layout(pathname, search)

    if pathname == PATH_LOGOUT:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, pcommon.layout(pathname, search)

    # =====================================================
    if pathname in PATH_SET_COMMON:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, pcommon.layout(pathname, search)

    # =====================================================
    if pathname in PATH_SET_MINE:
        if not flask_login.current_user.is_authenticated:
            return pathname, pcommon.layout(PATH_LOGIN, search)
        return pathname, pmine.layout(pathname, search)

    # =====================================================
    if pathname in PATH_SET_SYSTEM:
        if not flask_login.current_user.is_authenticated:
            return pathname, pcommon.layout(PATH_LOGIN, search)
        return pathname, psystem.layout(pathname, search)

    # =====================================================
    if pathname in PATH_SET_INDEX:
        return pathname, pindex.layout(pathname, search)

    # return 404 ==========================================
    return pathname, palert.layout_404(pathname, search)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8088, debug=True)
