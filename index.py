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
from pages import panalysis, pintros, puser
from utility import *

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
def _init_page(pathname, search, vhash, data_client):
    logging.warning("pathname=%s, search=%s, hash=%s, data_client=%s", pathname, search, vhash, data_client)

    # define variables
    kwargs = dict(vhash=vhash, data_client=data_client)
    data_server = dict(title=pathname.strip("/").upper())

    # =============================================================================================
    if pathname == PATH_INTROS or pathname == PATH_ROOT:
        return pathname, search, data_server, pintros.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_ANALYSIS:
        return pathname, search, data_server, panalysis.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_LOGIN or pathname == PATH_LOGOUT:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, data_server, plogin.layout(pathname, search, **kwargs)

    # =============================================================================================
    if pathname == PATH_REGISTERE or pathname == PATH_RESETPWDE:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, data_server, pemail.layout(pathname, search, **kwargs)

    if pathname == f"{PATH_REGISTERE}/result" or pathname == f"{PATH_RESETPWDE}/result":
        return pathname, search, data_server, palert.layout(pathname, search, **dict(
            text_hd="Sending success",
            text_sub=f"An email has sent to {flask.session.get('email')}.",
            text_button="Back to home",
            return_href=PATH_ROOT,
        ))

    # =============================================================================================
    if pathname == f"{PATH_REGISTERE}-pwd" or pathname == f"{PATH_RESETPWDE}-pwd":
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, data_server, ppwd.layout(pathname, search, **kwargs)

    if pathname == f"{PATH_REGISTERE}-pwd/result" or pathname == f"{PATH_RESETPWDE}-pwd/result":
        return pathname, search, data_server, palert.layout(pathname, search, **dict(
            text_hd="Setting success",
            text_sub="The password was set successfully.",
            text_button="Go to login",
            return_href=PATH_LOGIN,
        ))

    # =============================================================================================
    if pathname == PATH_USER:
        if not flask_login.current_user.is_authenticated:
            pathname = PATH_LOGIN
            kwargs.update(nextpath=PATH_USER)
            data_server = dict(title=pathname.strip("/").upper())
            return pathname, search, data_server, plogin.layout(pathname, search, **kwargs)
        return pathname, search, data_server, puser.layout(pathname, search, **kwargs)

    # =============================================================================================
    data_server = dict(title="error: 404")
    return pathname, search, data_server, palert.layout_404(pathname, search, return_href=PATH_ROOT)


# clientside callback
app.clientside_callback(
    """
    function(data) {
        document.title = data.title || '%s'
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
        }
        return href
    }
    """,
    Output({"type": "id-address", "index": MATCH}, "data"),
    Input({"type": "id-address", "index": MATCH}, "href"),
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8088, debug=True)
