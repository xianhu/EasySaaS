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

from app import UserLogin
from utility.consts import RE_EMAIL
from utility.paths import PATH_SIGNUP, PATH_FORGOTPWD, PATH_ROOT
from . import ERROR_EMAIL_FORMAT, ERROR_EMAIL_NOTEXIST, ERROR_PWD_INCORRECT
from . import LABEL_EMAIL, LABEL_PWD, LINK_REGISTER, LINK_FORGETPWD
from . import LOGIN_TEXT_HD, LOGIN_TEXT_SUB, LOGIN_TEXT_BUTTON
from . import tsign

TAG = "login"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    form_items = dbc.Form(children=[
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email"),
            dbc.Label(f"{LABEL_EMAIL}:", html_for=f"id-{TAG}-email"),
        ], class_name=None),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd", type="password"),
            dbc.Label(f"{LABEL_PWD}:", html_for=f"id-{TAG}-pwd"),
        ], class_name="mt-4"),
    ], class_name=None)

    # define args
    kwargs_temp = dict(
        src_image="illustrations/login.svg",
        text_hd=LOGIN_TEXT_HD,
        text_sub=LOGIN_TEXT_SUB,
        form_items=form_items,
        text_button=LOGIN_TEXT_BUTTON,
        other_list=[
            html.A(LINK_REGISTER, href=PATH_SIGNUP),
            html.A(LINK_FORGETPWD, href=PATH_FORGOTPWD),
        ],
        data=kwargs.get("nextpath", PATH_ROOT),
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


@dash.callback([
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
        return ERROR_EMAIL_FORMAT, dash.no_update
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = UserLogin.query.get(_id)
    if not user:
        return ERROR_EMAIL_NOTEXIST, dash.no_update

    # check password
    if not security.check_password_hash(user.pwd, pwd or ""):
        return ERROR_PWD_INCORRECT, dash.no_update

    # login user
    flask_login.login_user(user)

    # return result
    return None, nextpath
