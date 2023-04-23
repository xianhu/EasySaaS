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
from core.consts import *
from core.paths import *
from pages import palert, panalysis, pprojects, puser
from pages.dsign import pemail, plogin, psetpwd

# application layout
app.layout = html.Div(children=[
    html.Div(id="id-content"),
    # define components
    fuc.FefferyExecuteJs(id="id-executejs"),
    dcc.Location(id="id-location", refresh=False),
], className="bg-main overflow-auto overflow-x-hidden")


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
    # user instance
    current_user = flask_login.current_user

    # logging current_user
    xwho = current_user.id if current_user.is_authenticated else "Anonymous"
    logging.warning("[%s]: pathname=%s, search=%s, hash=%s", xwho, pathname, search, vhash)

    # define variables
    kwargs = dict(vhash=vhash, nextpath=None)
    jsstr_login = FMT_EXECUTEJS_HREF.format(href=PATH_LOGIN)
    jsstr_title = FMT_EXECUTEJS_TITLE.format(title=pathname.strip("/").upper())

    # =============================================================================================
    if pathname == PATH_LOGIN:
        if current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, plogin.layout(pathname, search, **kwargs), jsstr_title

    # =============================================================================================
    if pathname == PATH_SIGNUP or pathname == PATH_FORGOTPWD:
        if current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, pemail.layout(pathname, search, **kwargs), jsstr_title

    if pathname == f"{PATH_SIGNUP}/result" or pathname == f"{PATH_FORGOTPWD}/result":
        return pathname, search, pemail.layout_result(pathname, search, **kwargs), jsstr_title

    # =============================================================================================
    if pathname == f"{PATH_SIGNUP}-setpwd" or pathname == f"{PATH_FORGOTPWD}-setpwd":
        if current_user.is_authenticated:
            flask_login.logout_user()
        return pathname, search, psetpwd.layout(pathname, search, **kwargs), jsstr_title

    if pathname == f"{PATH_SIGNUP}-setpwd/result" or pathname == f"{PATH_FORGOTPWD}-setpwd/result":
        return pathname, search, psetpwd.layout_result(pathname, search, **kwargs), jsstr_title

    # =============================================================================================
    if pathname == PATH_ROOT:
        return pathname, search, dash.no_update, FMT_EXECUTEJS_HREF.format(href=PATH_PROJECTS)

    if pathname == PATH_USER:
        if not current_user.is_authenticated:
            return pathname, search, dash.no_update, jsstr_login
        return pathname, search, puser.layout(pathname, search, **kwargs), jsstr_title

    if pathname == PATH_PROJECTS:
        if not current_user.is_authenticated:
            return pathname, search, dash.no_update, jsstr_login
        return pathname, search, pprojects.layout(pathname, search, **kwargs), jsstr_title

    if pathname == PATH_ANALYSIS:
        if not current_user.is_authenticated:
            return pathname, search, dash.no_update, jsstr_login
        return pathname, search, panalysis.layout(pathname, search, **kwargs), jsstr_title

    # =============================================================================================
    return pathname, search, palert.layout_404(pathname, search, return_href=PATH_ROOT), jsstr_title


if __name__ == "__main__":
    # app.run_server(port=8000, debug=True)
    server.run(port=8000, debug=True)
