# _*_ coding: utf-8 _*_

"""
Application Layout
"""

import logging

import dash
import dash_bootstrap_components as dbc
import feffery_utils_components as fuc
import flask_login
from dash import Input, Output, State, dcc, html

from app import app, server
from config import config_app_name
from pages import palert, panalysis0, panalysis1
from pages.dsign import plogin, pemail, psetpwd
from utility.consts import *
from utility.paths import *

# application layout
app.title = config_app_name
app.layout = html.Div(children=[
    html.Div(id="id-content", className=None),
    # define components
    fuc.FefferyExecuteJs(id="id-executejs"),
    dcc.Location(id="id-location", refresh=False),
])

# complete layout
app.validation_layout = dbc.Container([])


@dash.callback([
    Output("id-location", "pathname"),
    Output("id-location", "search"),
    Output("id-executejs", "jsString"),
    Output("id-content", "children"),
], [
    Input("id-location", "pathname"),
    State("id-location", "search"),
    State("id-location", "hash"),
], prevent_initial_call=False)
def _init_page(pathname, search, vhash):
    logging.warning("pathname=%s, search=%s, hash=%s", pathname, search, vhash)

    # define variables
    kwargs = dict(vhash=vhash, nextpath=None)
    js_str = FMT_EXECUTEJS_TITLE.format(title=pathname.strip("/").upper())

    # =============================================================================================
    if pathname == PATH_LOGIN:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, js_str, plogin.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_SIGNUP or pathname == PATH_FORGOTPWD:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, js_str, pemail.layout(pathname, search, **kwargs)

    if pathname == f"{PATH_SIGNUP}/result" or pathname == f"{PATH_FORGOTPWD}/result":
        return pathname, search, js_str, pemail.layout_result(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == f"{PATH_SIGNUP}-setpwd" or pathname == f"{PATH_FORGOTPWD}-setpwd":
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, js_str, psetpwd.layout(pathname, search, **kwargs)

    if pathname == f"{PATH_SIGNUP}-setpwd/result" or pathname == f"{PATH_FORGOTPWD}-setpwd/result":
        return pathname, search, js_str, psetpwd.layout_result(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_ANALYSIS0 or pathname == PATH_ROOT:
        if not flask_login.current_user.is_authenticated:
            js_str = FMT_EXECUTEJS_HREF.format(href=PATH_LOGIN)
            return pathname, search, js_str, dash.no_update
        return pathname, search, js_str, panalysis0.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_ANALYSIS1:
        if not flask_login.current_user.is_authenticated:
            js_str = FMT_EXECUTEJS_HREF.format(href=PATH_LOGIN)
            return pathname, search, js_str, dash.no_update
        return pathname, search, js_str, panalysis1.layout(pathname, search, **kwargs)

    # =============================================================================================
    return pathname, search, js_str, palert.layout_404(pathname, search, return_href=PATH_ROOT)


if __name__ == "__main__":
    # app.run_server(host="0.0.0.0", port=8088)
    server.run(host="0.0.0.0", port=8088, debug=True)
