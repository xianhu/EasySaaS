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
from pages import palert, pemail, plogin, psetpwd
from pages import panalysis0, panalysis1
from utility.consts import FMT_EXECUTEJS
from utility.paths import *

# application layout
app.title = config_app_name
app.layout = html.Div(children=[
    html.Div(id="id-content", className=None),
    # define components
    dcc.Location(id="id-location", refresh=False),
    dcc.Store(id="id-store-client", storage_type="session"),
    dcc.Store(id="id-store-server", storage_type="session"),
])

# complete layout
app.validation_layout = dbc.Container([])


@dash.callback([
    Output("id-location", "pathname"),
    Output("id-location", "search"),
    Output("id-store-server", "data"),
    Output("id-content", "children"),
], [
    Input("id-location", "pathname"),
    State("id-location", "search"),
    State("id-location", "hash"),
    State("id-store-client", "data"),
], prevent_initial_call=False)
def _init_page(pathname, search, vhash, dclient):
    logging.warning("pathname=%s, search=%s, hash=%s, dclient=%s", pathname, search, vhash, dclient)

    # define variables
    kwargs = dict(vhash=vhash, dclient=dclient)
    dserver = dict(title=pathname.strip("/").upper())

    # =============================================================================================
    if pathname == PATH_LOGIN:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, dserver, plogin.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_SIGNUP or pathname == PATH_FORGOTPWD:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, dserver, pemail.layout(pathname, search, **kwargs)

    if pathname == f"{PATH_SIGNUP}/result" or pathname == f"{PATH_FORGOTPWD}/result":
        return pathname, search, dserver, pemail.layout_result(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == f"{PATH_SIGNUP}-setpwd" or pathname == f"{PATH_FORGOTPWD}-setpwd":
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, dserver, psetpwd.layout(pathname, search, **kwargs)

    if pathname == f"{PATH_SIGNUP}-setpwd/result" or pathname == f"{PATH_FORGOTPWD}-setpwd/result":
        return pathname, search, dserver, psetpwd.layout_result(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_ANALYSIS0 or pathname == PATH_ROOT:
        if not flask_login.current_user.is_authenticated:
            js_string = FMT_EXECUTEJS.format(href=PATH_LOGIN)
            return pathname, search, dserver, fuc.FefferyExecuteJs(jsString=js_string)
        return pathname, search, dserver, panalysis0.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_ANALYSIS1:
        if not flask_login.current_user.is_authenticated:
            js_string = FMT_EXECUTEJS.format(href=PATH_LOGIN)
            return pathname, search, dserver, fuc.FefferyExecuteJs(jsString=js_string)
        return pathname, search, dserver, panalysis1.layout(pathname, search, **kwargs)

    # =============================================================================================
    return pathname, search, dserver, palert.layout_404(pathname, search, return_href=PATH_ROOT)


# clientside callback
app.clientside_callback(
    """
    function(dserver) {
        document.title = dserver.title || '%s'
        return {
            'iwidth': window.innerWidth,
            'iheight': window.innerHeight,
        }
    }
    """ % config_app_name,
    Output("id-store-client", "data"),
    Input("id-store-server", "data"),
)

if __name__ == "__main__":
    # app.run_server(host="0.0.0.0", port=8088)
    server.run(host="0.0.0.0", port=8088, debug=True)
