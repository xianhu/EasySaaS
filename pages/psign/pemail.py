# _*_ coding: utf-8 _*_

"""
page of email
"""

import json
import uuid
import hashlib

import flask
import flask_mail
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from app import User, app, app_mail, app_redis
from config import config_app_domain, config_app_name
from utility.address import AddressAIO
from utility.consts import RE_EMAIL

from ..paths import *

TAG = "email"
ADDRESS = AddressAIO(f"id-{TAG}-address")


def layout(pathname, search):
    """
    layout of page
    """
    # define text and components
    if pathname == PATH_REGISTERE:
        text_hd, text_button = "Sign up", "Verify the email"
        text_sub = "Register an account through an email."
        image = html.Img(src="assets/illustrations/register.svg", className="img-fluid")
    else:
        text_hd, text_button = "Forget password?", "Verify the email"
        text_sub = "Find back the password through email."
        image = html.Img(src="assets/illustrations/resetpwd.svg", className="img-fluid")

    # define components
    form_children = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-email", type="email"),
        dbc.Label("Email:", html_for=f"id-{TAG}-email"),
    ])

    # define components
    other_addresses = [
        html.A("Sign in", href=PATH_LOGIN),
        html.A("Forget password?", href=PATH_RESETPWDE),
    ] if pathname == PATH_REGISTERE else [
        html.A("Sign in", href=PATH_LOGIN),
        html.A("Sign up", href=PATH_REGISTERE),
    ]

    # return result
    class_label = "text-danger text-center w-100 my-0"
    args_button = {"size": "lg", "class_name": "w-100 mt-4"}
    return html.Div(children=[
        ADDRESS, dcc.Store(id=f"id-{TAG}-pathname", data=pathname),

        html.A(children=[
            html.Img(src="assets/favicon.png", style={"width": "1.25rem"}),
            html.Span(config_app_name, className="fs-5 text-primary align-middle"),
        ], href="/", className="text-decoration-none position-absolute top-0 start-0"),

        dbc.Row(children=[
            dbc.Col(image, width=10, md=4, class_name="mt-auto mt-md-0"),
            dbc.Col(children=[
                html.Div(text_hd, className="text-center fs-1"),
                html.Div(text_sub, className="text-center text-muted"),

                dbc.Form(form_children, class_name="mt-4"),
                dbc.Label(id=f"id-{TAG}-label", hidden=True, class_name=class_label),

                dbc.Button(text_button, id=f"id-{TAG}-button", **args_button),
                html.Div(other_addresses, className="d-flex justify-content-between"),
            ], width=10, md={"size": 3, "offset": 1}, class_name="mb-auto mb-md-0"),
        ], align="center", justify="center", class_name="vh-100 w-100 mx-auto")
    ])


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
    if pathname == PATH_REGISTERE and user:
        return "Email is registered", False, None
    if pathname == PATH_RESETPWDE and (not user):
        return "Email doesn't exist", False, None

    # send email and cache
    if not app_redis.get(_id):
        token = str(uuid.uuid4())
        path_pwd = f"{pathname}-pwd?{_id}&&{token}"

        if pathname == PATH_REGISTERE:
            subject = f"Registration of {config_app_name}"
        else:
            subject = f"Resetting password of {config_app_name}"
        body = f"please click link in 10 minutes: {config_app_domain}{path_pwd}"
        app_mail.send(flask_mail.Message(subject, body=body, recipients=[email, ]))

        # cache data
        app_redis.set(_id, json.dumps([token, email]), ex=60 * 10)

    # set session
    flask.session["email"] = email

    # return result
    return None, True, f"{pathname}/result"
