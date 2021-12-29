# _*_ coding: utf-8 _*_

"""
password page
"""

import json
import hashlib
import logging

import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from werkzeug import security

from app import User, app, app_db, app_redis
from config import config_app_name
from utility.address import AddressAIO
from utility.consts import RE_PWD

from .. import palert
from ..paths import *

TAG = "password"
ADDRESS = AddressAIO(f"id-{TAG}-address")


def layout(pathname, search):
    """
    layout of page
    """
    try:
        _id, _token = [item.strip() for item in search.strip().split("&&")]
        token, email = json.loads(app_redis.get(_id))
        assert _token == token, (_token, token)
    except Exception as excep:
        logging.error("token expired or error: %s", excep)
        text_sub = "The link has already expired, click button to safe page."
        return palert.layout_simple("Link expired", text_sub, "Back to safety", PATH_INTROS)

    # define text and components
    text_hd, text_button = "Set password", "Set password"
    text_sub = "Set the password of this email please."
    image = html.Img(src="assets/illustrations/password.svg", className="img-fluid")

    # define components
    form_children = [
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email", value=email, disabled=True),
            dbc.Label("Email:", html_for=f"id-{TAG}-email"),
        ]),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd1", type="password"),
            dbc.Label("Password:", html_for=f"id-{TAG}-pwd1"),
        ], class_name="mt-4"),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd2", type="password"),
            dbc.Label("Confirm Password:", html_for=f"id-{TAG}-pwd2"),
        ], class_name="mt-4"),
    ]

    # define components
    other_addresses = [
        html.A("Sign in", href=PATH_LOGIN),
        html.A("Sign up", href=PATH_REGISTERE),
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
    State(f"id-{TAG}-pwd1", "value"),
    State(f"id-{TAG}-pwd2", "value"),
    State(f"id-{TAG}-pathname", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd1, pwd2, pathname):
    # check data
    if (not pwd1) or (len(pwd1) < 6):
        return "Password is too short", None
    if not RE_PWD.match(pwd1):
        return "Password must contain numbers and letters", None
    if (not pwd2) or (pwd2 != pwd1):
        return "Passwords are inconsistent", None
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = User.query.filter_by(id=_id).first()
    if not user:
        user = User(id=_id, email=email)
    user.pwd = security.generate_password_hash(pwd1)

    # commit user
    app_db.session.merge(user)
    app_db.session.commit()

    # delete cache
    app_redis.delete(_id)

    # return result
    return None, f"{pathname}/result"
