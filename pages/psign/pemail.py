# _*_ coding: utf-8 _*_

"""
email page
"""

import hashlib
import json
import urllib.parse
import uuid

import dash_bootstrap_components as dbc
import flask
import flask_mail
from dash import Input, Output, State, html

from app import User, app, app_mail, app_redis
from config import config_app_domain, config_app_name
from utility.consts import RE_EMAIL
from . import ptemplate
from ..paths import *

TAG = "sign-email"


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    form_items = dbc.Form(dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-email", type="email"),
        dbc.Label("Email:", html_for=f"id-{TAG}-email"),
    ]))

    # define parames
    if pathname == PATH_REGISTERE:
        params = {
            "image_src": "illustrations/register.svg",
            "text_hd": "Sign up",
            "text_sub": "Register an account through an email.",
            "form_items": form_items,
            "text_button": "Verify the email",
            "other_list": [
                html.A("Sign in", href=PATH_LOGIN),
                html.A("Forget password?", href=PATH_RESETPWDE),
            ],
        }
    else:
        params = {
            "image_src": "illustrations/resetpwd.svg",
            "text_hd": "Forget password?",
            "text_sub": "Find back the password through email.",
            "form_items": form_items,
            "text_button": "Verify the email",
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
    State(f"id-{TAG}-pathname", "data"),
    State(f"id-{TAG}-search", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pathname, search):
    # check data
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        return "Email is invalid", None
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = User.query.get(_id)
    if pathname == PATH_REGISTERE and user:
        return "Email is registered", None
    if pathname == PATH_RESETPWDE and (not user):
        return "Email doesn't exist", None

    # send email and cache
    if not app_redis.get(_id):
        token = str(uuid.uuid4())
        data = {
            "_id": _id,
            "token": token,
        }
        path_pwd = f"{pathname}-pwd?{urllib.parse.urlencode(data)}"

        if pathname == PATH_REGISTERE:
            subject = f"Registration of {config_app_name}"
        else:
            subject = f"Resetting password of {config_app_name}"
        body = f"please click link in 10 minutes: {config_app_domain}{path_pwd}"
        app_mail.send(flask_mail.Message(subject, body=body, recipients=[email, ]))

        # cache data
        app_redis.set(_id, json.dumps([token, email]), ex=60 * 10)

    # set session
    flask.session["email"] = email

    # return result
    return None, f"{pathname}/result"
