# _*_ coding: utf-8 _*_

"""
Application Layout
"""

import logging
import urllib.parse

import dash
import dash_bootstrap_components as dbc
import flask
import flask_login
from dash import Input, Output, State, MATCH, dcc, html

from app import app
from config import config_app_name
from pages import palert, pemail, plogin, ppwd
from pages import puser, pintros, panalysis
from pages.paths import *

# app layout
app.title = config_app_name
app.layout = html.Div(children=[
    html.Div(id="id-content", className=None),
    dcc.Location(id="id-location", refresh=False),
    dcc.Store(id="id-store-client", storage_type="session"),
    dcc.Store(id="id-store-dummpy", storage_type="session"),
])

# complete layout
app.validation_layout = dbc.Container([])


@app.callback([
    Output("id-location", "pathname"),
    Output("id-content", "children"),
    Output("id-store-client", "data"),
], [
    Input("id-location", "pathname"),
    State("id-location", "search"),
    State("id-store-client", "data"),
], prevent_initial_call=False)
def _init_page(pathname, search, data_client):
    logging.warning("pathname=%s, search=%s, data_client=%s", pathname, search, data_client)

    # define variables
    pathname = PATH_INTROS if pathname == "/" else pathname
    search = urllib.parse.parse_qs(search.lstrip("?").strip())

    # =========================================================================
    if pathname == PATH_INTROS:
        data_client = {"title": pathname.strip("/")}
        return pathname, pintros.layout(pathname, search), data_client

    # =========================================================================
    if pathname == PATH_LOGIN or pathname == PATH_LOGOUT:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        pathname = PATH_LOGIN
        search["next"] = [PATH_ANALYSIS, ]
        data_client = {"title": pathname.strip("/")}
        return pathname, plogin.layout(pathname, search), data_client

    # =========================================================================
    if pathname == PATH_REGISTERE or pathname == PATH_RESETPWDE:
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        data_client = {"title": pathname.strip("/")}
        return pathname, pemail.layout(pathname, search), data_client

    if pathname == f"{PATH_REGISTERE}/result" or pathname == f"{PATH_RESETPWDE}/result":
        args = {
            "text_hd": "Sending success",
            "text_sub": f"An email has sent to {flask.session.get('email')}.",
            "text_button": "Back to home",
            "return_href": PATH_INTROS,
        }
        data_client = {"title": pathname.strip("/")}
        return pathname, palert.layout(pathname, search, **args), data_client

    # =========================================================================
    if pathname == f"{PATH_REGISTERE}-pwd" or pathname == f"{PATH_RESETPWDE}-pwd":
        if flask_login.current_user.is_authenticated:
            flask_login.logout_user()
        data_client = {"title": pathname.strip("/")}
        return pathname, ppwd.layout(pathname, search), data_client

    if pathname == f"{PATH_REGISTERE}-pwd/result" or pathname == f"{PATH_RESETPWDE}-pwd/result":
        args = {
            "text_hd": "Setting success",
            "text_sub": "The password was set successfully.",
            "text_button": "Go to login",
            "return_href": PATH_LOGIN,
        }
        data_client = {"title": pathname.strip("/")}
        return pathname, palert.layout(pathname, search, **args), data_client

    # =========================================================================
    if pathname.startswith(PATH_USER):
        if not flask_login.current_user.is_authenticated:
            pathname = PATH_LOGIN
            search["next"] = [PATH_USER, ]
            data_client = {"title": pathname.strip("/")}
            return pathname, plogin.layout(pathname, search), data_client
        data_client = {"title": pathname.strip("/")}
        return pathname, puser.layout(pathname, search), data_client

    # =========================================================================
    if pathname.startswith(PATH_ANALYSIS):
        if not flask_login.current_user.is_authenticated:
            pathname = PATH_LOGIN
            search["next"] = [PATH_ANALYSIS, ]
            data_client = {"title": pathname.strip("/")}
            return pathname, plogin.layout(pathname, search), data_client
        data_client = {"title": pathname.strip("/")}
        return pathname, panalysis.layout(pathname, search), data_client

    # return 404 ==============================================================
    data_client = {"title": "error: 404"}
    return pathname, palert.layout_404(pathname, search, return_href=PATH_INTROS), data_client


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

# clientside callback
dash.clientside_callback(
    """
    function(data) {
        document.title = data.title || '%s'
        return data
    }
    """ % config_app_name,
    Output("id-store-dummpy", "data"),
    Input("id-store-client", "data"),
    prevent_initial_call=True,
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8088, debug=True)
