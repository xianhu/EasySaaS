# _*_ coding: utf-8 _*_

"""
Application Layout
"""

import logging

import dash_bootstrap_components as dbc
import flask
import flask_login
from dash import Input, Output, State, MATCH, dcc, html

from app import app
from config import config_app_name
from pages import palert, pemail, plogin, ppwd
from pages import padmin, panalysis, pintros, puser
from utility.paths import *

# app layout
app.title = config_app_name
app.layout = html.Div(children=[
    html.Div(id="id-content", className=None),
    dcc.Location(id="id-location", refresh=False),
    dcc.Store(id="id-store-client", storage_type="session"),
    dcc.Store(id="id-store-server", storage_type="session"),
])

# complete layout
app.validation_layout = dbc.Container([])


@app.callback([
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
    if pathname == PATH_LOGIN or pathname == PATH_LOGOUT:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, dserver, plogin.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_REGISTER or pathname == PATH_RESETPWD:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, dserver, pemail.layout(pathname, search, **kwargs)

    if pathname == f"{PATH_REGISTER}/result" or pathname == f"{PATH_RESETPWD}/result":
        return pathname, search, dserver, palert.layout(pathname, search, **dict(
            text_hd="Sending success",
            text_sub=f"An email has sent to {flask.session.get('email')}.",
            text_button="Back to home",
            return_href=PATH_ROOT,
        ))

    # =============================================================================================
    if pathname == f"{PATH_REGISTER}-pwd" or pathname == f"{PATH_RESETPWD}-pwd":
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, dserver, ppwd.layout(pathname, search, **kwargs)

    if pathname == f"{PATH_REGISTER}-pwd/result" or pathname == f"{PATH_RESETPWD}-pwd/result":
        return pathname, search, dserver, palert.layout(pathname, search, **dict(
            text_hd="Setting success",
            text_sub="The password was set successfully.",
            text_button="Go to login",
            return_href=PATH_LOGIN,
        ))

    # =============================================================================================
    if pathname == PATH_INTROS or pathname == PATH_ROOT:
        pathname = PATH_INTROS
        dserver = dict(title=pathname.strip("/").upper())
        return pathname, search, dserver, pintros.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_ANALYSIS:
        if not flask_login.current_user.is_authenticated:
            pathname = PATH_LOGIN
            kwargs.update(dict(nextpath=PATH_ANALYSIS))
            dserver = dict(title=pathname.strip("/").upper())
            return pathname, search, dserver, plogin.layout(pathname, search, **kwargs)
        return pathname, search, dserver, panalysis.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_USER:
        if not flask_login.current_user.is_authenticated:
            pathname = PATH_LOGIN
            kwargs.update(dict(nextpath=PATH_USER))
            dserver = dict(title=pathname.strip("/").upper())
            return pathname, search, dserver, plogin.layout(pathname, search, **kwargs)
        return pathname, search, dserver, puser.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_ADMIN:
        if flask_login.current_user.is_authenticated and flask_login.current_user.admin:
            return pathname, search, dserver, padmin.layout(pathname, search, **kwargs)
        else:
            return pathname, search, dserver, palert.layout_403(pathname, search, return_href=PATH_ROOT)

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

# clientside callback
app.clientside_callback(
    """
    function(href) {
        if (href != null && href != undefined) {
            window.location.href = href
            if (href.endsWith('#')) {
                window.location.reload()
            }
        }
        return href
    }
    """,
    Output({"type": "id-address", "index": MATCH}, "data"),
    Input({"type": "id-address", "index": MATCH}, "href"),
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8088, debug=True)
