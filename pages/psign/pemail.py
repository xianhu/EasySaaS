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
from utility.address import AddressAIO
from utility.consts import RE_EMAIL

from ..paths import *

TAG = "email"
ADDRESS = AddressAIO(f"id-{TAG}-address")

# define args of components
ARGS_BUTTON_SUBMIT = {"size": "lg", "class_name": "w-100"}

# define class of components
CLASS_LABEL_ERROR = "text-danger text-center w-100 mx-auto my-0"

# define class of components
CLASS_DIV_CATALOG = "side-class bg-light border-bottom px-3 py-2"
CLASS_DIV_CONTENT = "d-flex flex-column flex-md-row h-100 overflow-scroll gx-0"

# define components
COMP_A_LOGIN = html.A("Sign in", href=PATH_LOGIN)
COMP_A_REGISTER = html.A("Sign up", href=PATH_REGISTER_E)
COMP_A_RESETPWD = html.A("Forget password?", href=PATH_RESETPWD_E)


def layout(pathname, search):
    """
    layout of page
    """
    # define text
    if pathname == PATH_REGISTER_E:
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
    col_main = [
        ADDRESS,
        dcc.Store(id=f"id-{TAG}-pathname", data=pathname),

        html.Div(text_hd, className="text-center fs-1"),
        html.Div(text_sub, className="text-center text-muted"),

        dbc.Form(dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email"),
            dbc.Label("Email:", html_for=f"id-{TAG}-email"),
        ]), class_name="mt-4"),

        dbc.Label(id=f"id-{TAG}-label", hidden=True, class_name="text-danger text-center w-100 mx-auto my-0"),
        dbc.Button("Verify the email", id=f"id-{TAG}-button", size="lg", class_name="w-100 mt-4"),

        html.Div(others, className="d-flex justify-content-between"),
    ]

    # define column main
    return dbc.Row(children=[
        dbc.Col(image, width=10, md=4, class_name="mt-auto mt-md-0"),
        dbc.Col(col_main, width=10, md={"size": 3, "offset": 1}, class_name="mb-auto mb-md-0"),
    ], align="center", justify="center", class_name="vh-100 w-100 mx-auto")


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
    if pathname == PATH_REGISTER_E and user:
        return "Email is registered", False, None
    if pathname == PATH_RESETPWD_E and (not user):
        return "Email doesn't exist", False, None

    # define variables
    token = str(uuid.uuid4())
    if pathname == PATH_REGISTER_E:
        path_result = f"{PATH_REGISTER_E}/result"
        path_pwd = f"{PATH_REGISTER_E}/pwd?{_id}&&{token}"
        subject = f"Registration of {config_app_name}"
    else:
        path_result = f"{PATH_RESETPWD_E}/result"
        path_pwd = f"{PATH_RESETPWD_E}/pwd?{_id}&&{token}"
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
