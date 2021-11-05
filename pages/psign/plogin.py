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
from utility.address import AddressAIO
from utility.consts import RE_EMAIL

from ..paths import *

TAG = "login"
ADDRESS = AddressAIO(f"id-{TAG}-address")


def layout(pathname, search):
    """
    layout of page
    """
    # define text
    text_hd, text_button = "Sign in", "Sign in"
    text_sub = "Login the system with your account."

    # define components
    image_src = "assets/illustrations/login.svg"
    image = html.Img(src=image_src, className="img-fluid")

    # define components
    form_children = [
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email"),
            dbc.Label("Email:", html_for=f"id-{TAG}-email"),
        ]),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd", type="password"),
            dbc.Label("Password:", html_for=f"id-{TAG}-pwd"),
        ], class_name="mt-4"),
    ]

    # define components
    other_addresses = [
        html.A("Sign up", href=PATH_REGISTERE),
        html.A("Forget password?", href=PATH_RESETPWDE),
    ]

    # return result
    class_label = "text-center text-danger w-100 my-0"
    return dbc.Row(children=[
        dbc.Col(image, width=10, md=4, class_name="mt-auto mt-md-0"),
        dbc.Col(children=[
            ADDRESS, dcc.Store(id=f"id-{TAG}-pathname", data=pathname),

            html.Div(text_hd, className="text-center fs-1"),
            html.Div(text_sub, className="text-center text-muted"),

            dbc.Form(form_children, class_name="mt-4"),
            dbc.Label(id=f"id-{TAG}-label", hidden=True, class_name=class_label),

            dbc.Button(text_button, id=f"id-{TAG}-button", size="lg", class_name="w-100 mt-4"),
            html.Div(other_addresses, className="d-flex justify-content-between"),
        ], width=10, md={"size": 3, "offset": 1}, class_name="mb-auto mb-md-0"),
    ], align="center", justify="center", class_name="vh-100 w-100 mx-auto")


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
