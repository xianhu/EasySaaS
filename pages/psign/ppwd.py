# _*_ coding: utf-8 _*_

"""
password page
"""

import json
import hashlib
import logging

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from werkzeug import security

from app import User, app, app_db, app_redis
from utility.consts import RE_PWD

from .. import palert
from ..paths import *
from . import ptemplate

TAG = "sign-pwd"


def layout(pathname, search):
    """
    layout of page
    """
    try:
        _id, _token = [item.strip() for item in search.split("&&")]
        token, email = json.loads(app_redis.get(_id))
        assert _token == token, (_token, token)
    except Exception as excep:
        logging.error("token expired or error: %s", excep)
        text_sub = "The link has already expired, click button to safe page."
        return palert.layout_simple("Link expired", text_sub, "Back to safety", PATH_INTROS)

    # define components
    form_items = dbc.Form(children=[
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email", value=email, disabled=True),
            dbc.Label("Email:", html_for=f"id-{TAG}-email"),
        ], class_name=None),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd1", type="password"),
            dbc.Label("Password:", html_for=f"id-{TAG}-pwd1"),
        ], class_name="mt-4"),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd2", type="password"),
            dbc.Label("Confirm Password:", html_for=f"id-{TAG}-pwd2"),
        ], class_name="mt-4"),
    ])

    # define parames
    params = {
        "image_src": "illustrations/password.svg",
        "text_hd": "Set password",
        "text_sub": "Set the password of this email please.",
        "form_items": form_items,
        "text_button": "Set password",
        "other_list": [
            html.A("Sign in", href=PATH_LOGIN),
            html.A("Sign up", href=PATH_REGISTERE),
        ],
    }

    # return result
    return ptemplate.layout(pathname, search, TAG, params)


@app.callback([
    Output(f"id-{TAG}-fb", "children"),
    Output({"type": "id-address", "index": TAG}, "href"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-email", "value"),
    State(f"id-{TAG}-pwd1", "value"),
    State(f"id-{TAG}-pwd2", "value"),
    State(f"id-{TAG}-pathname", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd1, pwd2, pathname):
    # check data
    if (not pwd1) or (len(pwd1) < 6):
        return "Password is too short", None
    if not RE_PWD.match(pwd1):
        return "Password must contain numbers and letters", None
    if (not pwd2) or (pwd2 != pwd1):
        return "Passwords are inconsistent", None
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
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
