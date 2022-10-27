# _*_ coding: utf-8 _*_

"""
login page
"""

import hashlib

import dash
import dash_bootstrap_components as dbc
import feffery_utils_components as fuc
import flask_login
from dash import Input, Output, State
from werkzeug import security

from app import UserLogin
from utility.consts import RE_EMAIL
from utility.paths import PATH_ROOT
from . import ERROR_EMAIL_FORMAT, ERROR_EMAIL_NOTEXIST, ERROR_PWD_INCORRECT
from . import LABEL_EMAIL, LABEL_PWD, A_SIGNUP, A_FORGOTPWD, ERROR_CPC_INCORRECT
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
        dbc.Row(children=[
            dbc.Col(dbc.Input(id=f"id-{TAG}-cpcinput", placeholder="captcha"), width=6),
            dbc.Col(fuc.FefferyCaptcha(id=f"id-{TAG}-cpcimage", charNum=4), width=6),
        ], align="center", class_name="mt-4"),
    ], class_name=None)

    # define args
    kwargs_temp = dict(
        src_image="illustrations/login.svg",
        text_hd=LOGIN_TEXT_HD,
        text_sub=LOGIN_TEXT_SUB,
        form_items=form_items,
        text_button=LOGIN_TEXT_BUTTON,
        other_list=[A_SIGNUP, A_FORGOTPWD],
        data=kwargs.get("nextpath", PATH_ROOT),
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


@dash.callback([
    Output(f"id-{TAG}-feedback", "children"),
    Output({"type": "id-address", "index": TAG}, "href"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    Input(f"id-{TAG}-email", "value"),
    Input(f"id-{TAG}-pwd", "value"),
    Input(f"id-{TAG}-cpcinput", "value"),
    State(f"id-{TAG}-cpcimage", "captcha"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd, cinput, vimage, nextpath):
    # check trigger
    trigger = dash.ctx.triggered_id
    if trigger in (f"id-{TAG}-email", f"id-{TAG}-pwd", f"id-{TAG}-cpcinput"):
        return None, dash.no_update

    # check captcha
    if cinput != vimage:
        return ERROR_CPC_INCORRECT, dash.no_update

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
    flask_login.login_user(user, remember=True)

    # return result
    return None, nextpath
