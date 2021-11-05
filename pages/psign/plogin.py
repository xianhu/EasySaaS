# _*_ coding: utf-8 _*_

"""
page of login
"""

import hashlib

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from app import User, app
from utility.address import AddressAIO
from utility.consts import RE_EMAIL
from werkzeug import security

from ..paths import *

TAG = "login"
ADDRESS = AddressAIO(f"id-{TAG}-address")


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    image = html.Img(src="assets/illustrations/login.png", className="img-fluid")

    # define components
    col_main = [
        ADDRESS,
        dcc.Store(id=f"id-{TAG}-pathname", data=pathname),

        html.Div("Sign in", className="text-center fs-1"),
        html.Div("Login the system with your account.", className="text-center text-muted"),

        dbc.Form(children=[
            dbc.FormFloating(children=[
                dbc.Input(id=f"id-{TAG}-email", type="email"),
                dbc.Label("Email:", html_for=f"id-{TAG}-email"),
            ]),
            dbc.FormFloating(children=[
                dbc.Input(id=f"id-{TAG}-pwd", type="password"),
                dbc.Label("Password:", html_for=f"id-{TAG}-pwd"),
            ], class_name="mt-4"),
        ], class_name="mt-4"),

        dbc.Label(id=f"id-{TAG}-label", hidden=True, class_name="text-danger text-center w-100 mx-auto my-0"),
        dbc.Button("Sign in", id=f"id-{TAG}-button", size="lg", class_name="w-100 mt-4"),

        html.Div(children=[
            html.A("Sign up", href=PATH_REGISTERE),
            html.A("Forget password?", href=PATH_RESETPWDE),
        ], className="d-flex justify-content-between"),
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
