# _*_ coding: utf-8 _*_

"""
page of email
"""

import hashlib
import json
import uuid

import flask
import flask_mail
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from app import User, app, app_mail, app_redis
from config import config_app_domain, config_app_name
from config import config_src_register, config_src_resetpwd
from layouts.adaptive import layout_two
from layouts.address import AddressAIO
from utility.consts import RE_EMAIL

from ..common import *
from ..paths import *

TAG = "email"
ADDRESS = AddressAIO(f"id-{TAG}-address")


def layout(pathname, search):
    """
    layout of page
    """
    # define text
    if pathname == PATH_EMAIL_REGISTER:
        text_hd = "Sign up"
        text_sub = "Register an account through an email."
        image = html.Img(src=config_src_register, className="img-fluid")
        others = [COMP_A_LOGIN, COMP_A_RESETPWD]
    else:
        text_hd = "Forget password?"
        text_sub = "Find back the password through email."
        image = html.Img(src=config_src_resetpwd, className="img-fluid")
        others = [COMP_A_LOGIN, COMP_A_REGISTER]
    button = dbc.Button("Verify the email", id=f"id-{TAG}-button", **ARGS_BUTTON_SUBMIT)

    # define components
    form = dbc.Form(children=[
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email"),
            dbc.Label("Email:", html_for=f"id-{TAG}-email"),
        ]),
        dbc.Label(id=f"id-{TAG}-label", hidden=True, class_name=CLASS_LABEL_ERROR),
        dcc.Store(id=f"id-{TAG}-pathname", data=pathname),
        ADDRESS,
    ])

    # define column main
    col_main = layout_form(text_hd, text_sub, form, button, others)
    return layout_two(item_left=image, width_left=(10, 5, 5), item_right=col_main)


@app.callback([
    Output(f"id-{TAG}-label", "children"),
    Output(f"id-{TAG}-label", "hidden"),
    Output(f"id-{TAG}-address", "href"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-email", "value"),
    State(f"id-{TAG}-pathname", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pathname):
    # check data
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        return "Email is invalid", False, None
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = User.query.get(_id)
    if pathname == PATH_EMAIL_REGISTER and user:
        return "Email is registered", False, None
    if pathname == PATH_EMAIL_RESETPWD and (not user):
        return "Email doesn't exist", False, None

    # define variables
    token = str(uuid.uuid4())
    if pathname == PATH_EMAIL_REGISTER:
        path_result = PATH_EMAIL_REGISTER_RESULT
        path_pwd = f"{PATH_EMAIL_REGISTER_PWD}?{_id}&&{token}"
        subject = f"Registration of {config_app_name}"
    else:
        path_result = PATH_EMAIL_RESETPWD_RESULT
        path_pwd = f"{PATH_EMAIL_RESETPWD_PWD}?{_id}&&{token}"
        subject = f"Resetting password of {config_app_name}"

    # send email and cache
    if not app_redis.get(_id):
        body = f"please click link in 10 minutes: {config_app_domain}{path_pwd}"
        app_mail.send(flask_mail.Message(subject, body=body, recipients=[email, ]))
        app_redis.set(_id, json.dumps([token, email]), ex=60 * 10)

    # set session
    flask.session["email"] = email

    # return result
    return None, True, path_result
