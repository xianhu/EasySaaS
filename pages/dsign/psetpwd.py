# _*_ coding: utf-8 _*_

"""
set password page
"""

import hashlib
import json
import logging
import urllib.parse

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State
from werkzeug import security

from app import app_db, app_redis
from model import User
from utility.consts import RE_PWD
from utility.paths import PATH_LOGIN, PATH_ROOT
from . import ERROR_PWD_SHORT, ERROR_PWD_FORMAT, ERROR_PWD_INCONSISTENT
from . import LABEL_EMAIL, LABEL_PWD, LABEL_PWD_CFM
from . import SETPWD_TEXT_HD, SETPWD_TEXT_SUB, SETPWD_TEXT_BUTTON
from . import tsign
from .. import palert

TAG = "set-pwd"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    try:
        # get values from search
        search = urllib.parse.parse_qs(search.lstrip("?").strip())
        _id, _token = search.get("_id")[0], search.get("token")[0]

        # get values from redis
        token, email = json.loads(app_redis.get(_id))

        # verify token values
        assert token == _token, (token, _token)
    except Exception as excep:
        logging.error("token expired or error: %s", excep)
        return palert.layout_expired(pathname, search, return_href=PATH_ROOT)

    # define components
    form_items = dbc.Form(children=[
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email", value=email, readonly=True),
            dbc.Label(f"{LABEL_EMAIL}:", html_for=f"id-{TAG}-email"),
        ], class_name=None),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd1", type="password"),
            dbc.Label(f"{LABEL_PWD}:", html_for=f"id-{TAG}-pwd1"),
        ], class_name="mt-4"),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd2", type="password"),
            dbc.Label(f"{LABEL_PWD_CFM}:", html_for=f"id-{TAG}-pwd2"),
        ], class_name="mt-4"),
    ], class_name=None)

    # define args
    kwargs_temp = dict(
        src_image="illustrations/setpwd.svg",
        text_hd=SETPWD_TEXT_HD,
        text_sub=SETPWD_TEXT_SUB,
        form_items=form_items,
        text_button=SETPWD_TEXT_BUTTON,
        other_list=[],
        data=pathname,
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


def layout_result(pathname, search, **kwargs):
    """
    layout of page
    """
    return palert.layout(pathname, search, **dict(
        text_hd="Setting success",
        text_sub="The password was set successfully.",
        text_button="Go to login",
        return_href=PATH_LOGIN,
    ))


@dash.callback([
    Output(f"id-{TAG}-feedback", "children"),
    Output({"type": "id-address", "index": TAG}, "href"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    Input(f"id-{TAG}-email", "value"),
    Input(f"id-{TAG}-pwd1", "value"),
    Input(f"id-{TAG}-pwd2", "value"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd1, pwd2, pathname):
    # check trigger
    trigger = dash.ctx.triggered_id
    if trigger in (f"id-{TAG}-email", f"id-{TAG}-pwd1", f"id-{TAG}-pwd2"):
        return None, dash.no_update

    # check password
    if (not pwd1) or (len(pwd1) < 6):
        return ERROR_PWD_SHORT, dash.no_update
    if not RE_PWD.match(pwd1):
        return ERROR_PWD_FORMAT, dash.no_update
    if (not pwd2) or (pwd2 != pwd1):
        return ERROR_PWD_INCONSISTENT, dash.no_update

    # check user
    _id = hashlib.md5(email.encode()).hexdigest()
    user = User.query.filter_by(id=_id).first()
    if not user:
        user = User(id=_id, email=email)
    user.pwd = security.generate_password_hash(pwd1)

    # commit user
    app_db.session.merge(user)
    app_db.session.commit()

    # delete cache
    app_redis.delete(_id)

    # return result
    return None, f"{pathname}/result"
