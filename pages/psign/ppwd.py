# _*_ coding: utf-8 _*_

"""
page of password
"""

import hashlib
import json

import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from werkzeug import security

from app import User, app, app_db, app_redis
from utility.address import AddressAIO
from utility.consts import RE_PWD

from ..palert import layout_expire
from ..paths import *

TAG = "password"
ADDRESS = AddressAIO(f"id-{TAG}-address")


def layout(pathname, search):
    """
    layout of page
    """
    # check token is valid
    try:
        _id, _token = search.strip().split("&&")
        token, email = json.loads(app_redis.get(_id))
        assert _token == token
    except:
        return layout_expire(pathname, search, PATH_INTROS)

    # define text
    text_hd, text_button = "Set password", "Set password"
    text_sub = "Set the password of this email."

    # define components
    image_src = "assets/illustrations/password.svg"
    image = html.Img(src=image_src, className="img-fluid")

    # define components
    form_children = [
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email", value=email, disabled=True),
            dbc.Label("Email:", html_for=f"id-{TAG}-email"),
        ]),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd", type="password"),
            dbc.Label("Password:", html_for=f"id-{TAG}-pwd"),
        ], class_name="mt-4"),
        dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-pwd1", type="password"),
            dbc.Label("Confirm Password:", html_for=f"id-{TAG}-pwd1"),
        ], class_name="mt-4"),
    ]

    # define components
    other_addresses = [
        html.A("Sign in", href=PATH_LOGIN),
        html.A("Sign up", href=PATH_REGISTERE),
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
    State(f"id-{TAG}-pwd1", "value"),
    State(f"id-{TAG}-pathname", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd, pwd1, pathname):
    # check data
    if (not pwd) or (len(pwd) < 6):
        return "Password is too short", False, None
    if not RE_PWD.match(pwd):
        return "Password must contain numbers and letters", False, None
    if (not pwd1) or (pwd1 != pwd):
        return "Passwords are inconsistent", False, None
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = User.query.filter_by(id=_id).first()
    if not user:
        user = User(id=_id, email=email)
    user.pwd = security.generate_password_hash(pwd)

    # commit user data
    app_db.session.merge(user)
    app_db.session.commit()

    # delete cache
    app_redis.delete(_id)

    # return result
    return None, True, f"{pathname}-result"
