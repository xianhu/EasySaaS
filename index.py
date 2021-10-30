# _*_ coding: utf-8 _*_

"""
Layout
"""

import logging

import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, dcc

import pages.pasign.consts as cs_asign
import pages.pindex.consts as cs_index
import pages.pmine.consts as cs_mine
import pages.psys_analysis.consts as cs_analysis
from app import app, server
from config import config_app_name
from pages import palert, pasign, pindex, pmine, psys_analysis

# app layout
app.title = config_app_name
app.layout = dbc.Container(children=[
    dcc.Location(id="id-location", refresh=False),
    dcc.Store(id="id-session", storage_type="session"),
    dbc.Container(id="id-content", class_name="vh-100 d-flex flex-column"),
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
    if pathname == cs_asign.PATH_LOGIN:
        if flask_login.current_user.is_authenticated:
            pathname = cs_analysis.PATH_SYS_ANALYSIS_DEMO
            return pathname, psys_analysis.layout(pathname, search)
        return pathname, pasign.layout(pathname, search)

    if pathname == cs_asign.PATH_LOGOUT:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, pasign.layout(pathname, search)

    # =====================================================
    if pathname in cs_asign.PATH_SET:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, pasign.layout(pathname, search)

    # =====================================================
    if pathname in cs_mine.PATH_SET:
        if not flask_login.current_user.is_authenticated:
            return pathname, pasign.layout(cs_asign.PATH_LOGIN, search)
        return pathname, pmine.layout(pathname, search)

    # =====================================================
    if pathname in cs_analysis.PATH_SET:
        if not flask_login.current_user.is_authenticated:
            return pathname, pasign.layout(cs_asign.PATH_LOGIN, search)
        return pathname, psys_analysis.layout(pathname, search)

    # =====================================================
    if pathname in cs_index.PATH_SET:
        return pathname, pindex.layout(pathname, search)

    # return 404 ==========================================
    return pathname, palert.layout_404(pathname, search)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8088, debug=True)
