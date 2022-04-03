# _*_ coding: utf-8 _*_

"""
Application Layout
"""

import logging

import dash
import dash_bootstrap_components as dbc
import flask
import flask_login
from dash import Input, Output, State, MATCH, dcc, html

from app import app
from config import config_app_name
from pages import palert, pemail, plogin, ppwd
from pages import panalysis, pintros, puser
from utility.consts import *

# app layout
app.title = config_app_name
app.layout = html.Div(children=[
    html.Div(id="id-content", className=None),
    dcc.Location(id="id-location", refresh=False),
    dcc.Store(id="id-store-client", storage_type="session"),
    dcc.Store(id="id-store-iwidth", storage_type="session"),
])

# complete layout
app.validation_layout = dbc.Container([])


@app.callback([
    Output("id-location", "pathname"),
    Output("id-location", "search"),
    Output("id-store-client", "data"),
    Output("id-content", "children"),
], [
    Input("id-location", "pathname"),
    State("id-location", "search"),
    State("id-store-client", "data"),
    State("id-store-iwidth", "data"),
], prevent_initial_call=False)
def _init_page(pathname, search, dclient, diwidth):
    logging.warning("pathname=%s, search=%s, dclient=%s, diwidth=%s", pathname, search, dclient, diwidth)

    # define variables
    pathname = PATH_INTROS if pathname == PATH_ROOT else pathname

    # =============================================================================================
    if pathname == PATH_INTROS:
        dclient = {"title": pathname.strip("/").upper()}
        return pathname, search, dclient, pintros.layout(pathname, search)

    # =============================================================================================
    if pathname == PATH_ANALYSIS:
        dclient = {"title": pathname.strip("/").upper()}
        return pathname, search, dclient, panalysis.layout(pathname, search)

    # =============================================================================================
    if pathname == PATH_LOGIN or pathname == PATH_LOGOUT:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        pathname = PATH_LOGIN
        dclient = {"title": pathname.strip("/").upper()}
        return pathname, search, dclient, plogin.layout(pathname, search)

    # =============================================================================================
    if pathname == PATH_REGISTERE or pathname == PATH_RESETPWDE:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        dclient = {"title": pathname.strip("/").upper()}
        return pathname, search, dclient, pemail.layout(pathname, search)

    if pathname == f"{PATH_REGISTERE}/result" or pathname == f"{PATH_RESETPWDE}/result":
        dclient = {"title": pathname.strip("/").upper()}
        return pathname, search, dclient, palert.layout(pathname, search, **dict(
            text_hd="Sending success",
            text_sub=f"An email has sent to {flask.session.get('email')}.",
            text_button="Back to home",
            return_href=PATH_ROOT,
        ))

    # =============================================================================================
    if pathname == f"{PATH_REGISTERE}-pwd" or pathname == f"{PATH_RESETPWDE}-pwd":
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        dclient = {"title": pathname.strip("/").upper()}
        return pathname, search, dclient, ppwd.layout(pathname, search)

    if pathname == f"{PATH_REGISTERE}-pwd/result" or pathname == f"{PATH_RESETPWDE}-pwd/result":
        dclient = {"title": pathname.strip("/").upper()}
        return pathname, search, dclient, palert.layout(pathname, search, **dict(
            text_hd="Setting success",
            text_sub="The password was set successfully.",
            text_button="Go to login",
            return_href=PATH_LOGIN,
        ))

    # =============================================================================================
    if pathname == PATH_USER:
        if not flask_login.current_user.is_authenticated:
            pathname = PATH_LOGIN
            dclient = {"title": pathname.strip("/").upper()}
            return pathname, search, dclient, plogin.layout(pathname, search, next=PATH_USER)
        dclient = {"title": pathname.strip("/").upper()}
        return pathname, search, dclient, puser.layout(pathname, search)

    # =============================================================================================
    dclient = {"title": "error: 404"}
    return pathname, search, dclient, palert.layout_404(pathname, search, return_href=PATH_ROOT)


# clientside callback
dash.clientside_callback(
    """
    function(data) {
        document.title = data.title || '%s'
        return window.innerWidth
    }
    """ % config_app_name,
    Output("id-store-iwidth", "data"),
    Input("id-store-client", "data"),
    prevent_initial_call=True,
)

# clientside callback
dash.clientside_callback(
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
