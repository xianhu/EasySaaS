# _*_ coding: utf-8 _*_

"""
page of login
"""

import hashlib

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from werkzeug import security

from app import User, app
from config import config_src_login
from layouts.adaptive import layout_two
from layouts.address import AddressAIO
from utility.consts import RE_EMAIL

from ..common import *
from ..paths import *

TAG = "login"
ADDRESS = AddressAIO(f"id-{TAG}-address")


def layout(pathname, search):
    """
    layout of page
    """
    # define text
    text_hd = "Sign in"
    text_sub = "Login the system with your account."
    image = html.Img(src=config_src_login, className="img-fluid")

    # define components
    others = [COMP_A_REGISTER, COMP_A_RESETPWD]
    button = dbc.Button(text_hd, id=f"id-{TAG}-button", **ARGS_BUTTON_SUBMIT)

    # define components
    form = dbc.Form(children=[
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email"),
            dbc.Label("Email:", html_for=f"id-{TAG}-email"),
        ]),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd", type="password"),
            dbc.Label("Password:", html_for=f"id-{TAG}-pwd"),
        ], class_name="mt-4"),
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
    State(f"id-{TAG}-pwd", "value"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd):
    # check data
    email, pwd = (email or "").strip(), (pwd or "").strip()
    if not RE_EMAIL.match(email):
        return "Email is invalid", False, None
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = User.query.get(_id)
    if not user:
        return "Email doesn't exist", False, None
    if not security.check_password_hash(user.pwd, pwd):
        return "Password is incorrect", False, None

    # login user
    flask_login.login_user(user)

    # return result
    return None, True, PATH_ANALYSIS
