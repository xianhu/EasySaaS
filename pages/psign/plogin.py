# _*_ coding: utf-8 _*_

"""
login page
"""

import hashlib

import flask_login
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from werkzeug import security

from app import UserLogin, app
from config import config_app_name
from utility.address import AddressAIO
from utility.consts import RE_EMAIL

from ..paths import *

TAG = "login"
ADDRESS = AddressAIO(f"id-{TAG}-address")


def layout(pathname, search):
    """
    layout of page
    """
    # define text and components
    text_hd, text_button = "Sign in", "Sign in"
    text_sub = "Login the system with your account."
    image = html.Img(src="assets/illustrations/login.svg", className="img-fluid")

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
    args_button = {"size": "lg", "class_name": "w-100 mt-4"}
    return html.Div(children=[
        ADDRESS, dcc.Store(id=f"id-{TAG}-pathname", data=pathname),

        html.A(children=[
            html.Img(src="assets/favicon.svg", style={"width": "1.25rem"}),
            html.Span(config_app_name, className="fs-5 text-primary align-middle"),
        ], href="/", className="text-decoration-none position-absolute top-0 start-0"),

        dbc.Row(children=[
            dbc.Col(image, width=10, md=4, class_name="mt-auto mt-md-0"),
            dbc.Col(children=[
                html.Div(text_hd, className="text-center fs-1"),
                html.Div(text_sub, className="text-center text-muted"),

                dbc.Form(form_children, class_name="mt-4"),
                html.Div(id=f"id-{TAG}-fb", className="text-danger text-center"),

                dbc.Button(text_button, id=f"id-{TAG}-button", **args_button),
                html.Div(other_addresses, className="d-flex justify-content-between"),
            ], width=10, md={"size": 3, "offset": 1}, class_name="mb-auto mb-md-0"),
        ], align="center", justify="center", class_name="vh-100 w-100 mx-auto")
    ])


@app.callback([
    Output(f"id-{TAG}-fb", "children"),
    Output(f"id-{TAG}-address", "href"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-email", "value"),
    State(f"id-{TAG}-pwd", "value"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd):
    # check data
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        return "Email is invalid", None
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = UserLogin.query.get(_id)
    if not user:
        return "Email doesn't exist", None

    # check password
    if not security.check_password_hash(user.pwd, pwd or ""):
        return "Password is incorrect", None

    # login user
    flask_login.login_user(user)

    # return result
    return None, PATH_ANALYSIS
