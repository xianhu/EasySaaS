# _*_ coding: utf-8 _*_

"""
email page
"""

import hashlib
import json
import urllib.parse
import uuid

import dash
import dash_bootstrap_components as dbc
import flask
import flask_mail
from dash import Input, Output, State, html

from app import User, app_mail, app_redis
from config import config_app_domain, config_app_name
from pages.dsign import tsign
from utility.consts import RE_EMAIL
from utility.paths import PATH_LOGIN, PATH_REGISTER, PATH_RESETPWD

TAG = "email"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    form_items = dbc.Form(dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-email", type="email"),
        dbc.Label("Email:", html_for=f"id-{TAG}-email"),
    ]), class_name=None)

    # define args
    kwargs_temp = dict(
        src_image="illustrations/register.svg",
        text_hd="Sign up",
        text_sub="Register an account through an email.",
        form_items=form_items,
        text_button="Verify the email",
        other_list=[
            html.A("Sign in", href=PATH_LOGIN),
            html.A("Forget password?", href=PATH_RESETPWD),
        ],
        data=PATH_REGISTER,
    ) if pathname == PATH_REGISTER else dict(
        src_image="illustrations/resetpwd.svg",
        text_hd="Forget password?",
        text_sub="Find back the password through email.",
        form_items=form_items,
        text_button="Verify the email",
        other_list=[
            html.A("Sign in", href=PATH_LOGIN),
            html.A("Sign up", href=PATH_REGISTER),
        ],
        data=PATH_RESETPWD,
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


@dash.callback([
    Output(f"id-{TAG}-feedback", "children"),
    Output({"type": "id-address", "index": TAG}, "href"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-email", "value"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pathname):
    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        return "Email is invalid", dash.no_update
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = User.query.get(_id)
    if pathname == PATH_REGISTER and user:
        return "Email is registered", dash.no_update
    if pathname == PATH_RESETPWD and (not user):
        return "Email doesn't exist", dash.no_update

    # send email and cache
    if not app_redis.get(_id):
        token = str(uuid.uuid4())

        # define href of verify
        query_string = urllib.parse.urlencode(dict(_id=_id, token=token))
        href_verify = f"{config_app_domain}{pathname}-pwd?{query_string}"

        # send email
        if pathname == PATH_REGISTER:
            subject = f"Registration of {config_app_name}"
        else:
            subject = f"Resetting password of {config_app_name}"
        body = f"please click link in 10 minutes: {href_verify}"
        app_mail.send(flask_mail.Message(subject, body=body, recipients=[email, ]))

        # cache token and email
        app_redis.set(_id, json.dumps([token, email]), ex=60 * 10)

    # set session
    flask.session["email"] = email

    # return result
    return None, f"{pathname}/result"
