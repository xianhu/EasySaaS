# _*_ coding: utf-8 _*_

"""
Application Layout
"""

import logging

import dash
import feffery_utils_components as fuc
import flask_login
from dash import Input, Output, State, dcc, html

from app import app, server
from pages import palert, panalysis
from pages.dsign import plogin, pemail, psetpwd
from utility.consts import *
from utility.paths import *

# application layout
app.layout = html.Div(children=[
    html.Div(id="id-content"),
    # define components
    fuc.FefferyExecuteJs(id="id-executejs"),
    dcc.Location(id="id-location", refresh=False),
])


@dash.callback([
    Output("id-location", "pathname"),
    Output("id-location", "search"),
    Output("id-content", "children"),
    Output("id-executejs", "jsString"),
], [
    Input("id-location", "pathname"),
    State("id-location", "search"),
    State("id-location", "hash"),
], prevent_initial_call=False)
def _init_page(pathname, search, vhash):
    logging.warning("pathname=%s, search=%s, hash=%s", pathname, search, vhash)

    # define variables
    kwargs = dict(vhash=vhash, nextpath=None)
    js_str_login = FMT_EXECUTEJS_HREF.format(href=PATH_LOGIN)
    js_str_title = FMT_EXECUTEJS_TITLE.format(title=pathname.strip("/").upper())

    # =============================================================================================
    if pathname == PATH_LOGIN:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, plogin.layout(pathname, search, **kwargs), js_str_title

    # =============================================================================================
    if pathname == PATH_SIGNUP or pathname == PATH_FORGOTPWD:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, pemail.layout(pathname, search, **kwargs), js_str_title

    if pathname == f"{PATH_SIGNUP}/result" or pathname == f"{PATH_FORGOTPWD}/result":
        return pathname, search, pemail.layout_result(pathname, search, **kwargs), js_str_title

    # =============================================================================================
    if pathname == f"{PATH_SIGNUP}-setpwd" or pathname == f"{PATH_FORGOTPWD}-setpwd":
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, psetpwd.layout(pathname, search, **kwargs), js_str_title

    if pathname == f"{PATH_SIGNUP}-setpwd/result" or pathname == f"{PATH_FORGOTPWD}-setpwd/result":
        return pathname, search, psetpwd.layout_result(pathname, search, **kwargs), js_str_title

    # =============================================================================================
    if pathname == PATH_ROOT:
        return pathname, search, dash.no_update, FMT_EXECUTEJS_HREF.format(href=PATH_ANALYSIS)

    if pathname == PATH_ANALYSIS:
        if not flask_login.current_user.is_authenticated:
            return pathname, search, dash.no_update, js_str_login
        return pathname, search, panalysis.layout(pathname, search, **kwargs), js_str_title

    # =============================================================================================
    return pathname, search, palert.layout_404(pathname, search, return_href=PATH_ROOT), js_str_title


if __name__ == "__main__":
    # app.run_server(host="0.0.0.0", port=8088, debug=True)
    server.run(host="0.0.0.0", port=8088, debug=True)
