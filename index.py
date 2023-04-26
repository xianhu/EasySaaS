# _*_ coding: utf-8 _*_

"""
Application Layout
"""

import logging

import dash
import feffery_utils_components as fuc
from dash import Input, Output, State, dcc, html
from flask import session as flask_session

from app import app, server
from core.consts import *
from pages.paths import *
from core.security import get_access_sub
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
    # get user.id or None
    user_id = get_access_sub(flask_session.get("token", ""))
    logging.warning("[%s] pathname: %s, search: %s", user_id, pathname, search)

    # define variables
    kwargs = dict(vhash=vhash, user_id=user_id)
    jsstr_login = FMT_EXECUTEJS_HREF.format(href=PATH_LOGIN)
    jsstr_title = FMT_EXECUTEJS_TITLE.format(title=pathname.strip("/").upper())

    # =============================================================================================
    if pathname == PATH_LOGIN:
        if flask_session.get("token"):
            flask_session.pop("token")
        return pathname, search, plogin.layout(pathname, search, **kwargs), jsstr_title

    # =============================================================================================
    if pathname == PATH_SIGNUP or pathname == PATH_FORGOTPWD:
        if flask_session.get("token"):
            flask_session.pop("token")
        return pathname, search, pemail.layout(pathname, search, **kwargs), jsstr_title

    if pathname == f"{PATH_SIGNUP}/result" or pathname == f"{PATH_FORGOTPWD}/result":
        return pathname, search, pemail.layout_result(pathname, search, **kwargs), jsstr_title

    # =============================================================================================
    if pathname == f"{PATH_SIGNUP}-setpwd" or pathname == f"{PATH_FORGOTPWD}-setpwd":
        if flask_session.get("token"):
            flask_session.pop("token")
        return pathname, search, psetpwd.layout(pathname, search, **kwargs), jsstr_title

    if pathname == f"{PATH_SIGNUP}-setpwd/result" or pathname == f"{PATH_FORGOTPWD}-setpwd/result":
        return pathname, search, psetpwd.layout_result(pathname, search, **kwargs), jsstr_title

    # =============================================================================================
    if pathname == PATH_ROOT:
        return pathname, search, dash.no_update, FMT_EXECUTEJS_HREF.format(href=PATH_PROJECTS)

    if pathname == PATH_USER:
        if not user_id:
            return pathname, search, dash.no_update, jsstr_login
        return pathname, search, puser.layout(pathname, search, **kwargs), jsstr_title

    if pathname == PATH_PROJECTS:
        if not user_id:
            return pathname, search, dash.no_update, jsstr_login
        return pathname, search, pprojects.layout(pathname, search, **kwargs), jsstr_title

    if pathname == PATH_ANALYSIS:
        if not user_id:
            return pathname, search, dash.no_update, jsstr_login
        return pathname, search, panalysis.layout(pathname, search, **kwargs), jsstr_title

    # =============================================================================================
    return pathname, search, palert.layout_404(pathname, search, return_href=PATH_ROOT), jsstr_title


if __name__ == "__main__":
    # app.run_server(port=8000, debug=True)
    server.run(port=8000, debug=True)
