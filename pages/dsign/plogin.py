# _*_ coding: utf-8 _*_

"""
login page
"""

import hashlib

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, html
from werkzeug import security

from app import UserLogin, app
from utility.consts import RE_EMAIL
from utility.paths import PATH_REGISTER, PATH_RESETPWD, PATH_ROOT
from pages.dsign import tsign

TAG = "login"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    form_items = dbc.Form(children=[
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email"),
            dbc.Label("Email:", html_for=f"id-{TAG}-email"),
        ], class_name=None),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd", type="password"),
            dbc.Label("Password:", html_for=f"id-{TAG}-pwd"),
        ], class_name="mt-4"),
    ], class_name=None)

    # define args
    kwargs_temp = dict(
        src_image="illustrations/login.svg",
        text_hd="Sign in",
        text_sub="Login the system with your account.",
        form_items=form_items,
        text_button="Sign in",
        other_list=[
            html.A("Sign up", href=PATH_REGISTER),
            html.A("Forget password?", href=PATH_RESETPWD),
        ],
        data=kwargs.get("nextpath", PATH_ROOT),
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


@app.callback([
    Output(f"id-{TAG}-feedback", "children"),
    Output({"type": "id-address", "index": TAG}, "href"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-email", "value"),
    State(f"id-{TAG}-pwd", "value"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd, nextpath):
    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        return "Email is invalid", dash.no_update
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = UserLogin.query.get(_id)
    if not user:
        return "Email doesn't exist", dash.no_update

    # check password
    if not security.check_password_hash(user.pwd, pwd or ""):
        return "Password is incorrect", dash.no_update

    # login user
    flask_login.login_user(user)

    # return result
    return None, nextpath
