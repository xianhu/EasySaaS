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
from config import config_src_pwd
from layouts.adaptive import layout_two
from layouts.address import AddressAIO
from utility.consts import RE_PWD

from ..common import *
from ..paths import *
from ..palert import layout_expire

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
    text_hd = "Set password"
    text_sub = "Set the password of email."
    image = html.Img(src=config_src_pwd, className="img-fluid")

    # define components
    others = [COMP_A_LOGIN, COMP_A_REGISTER]
    button = dbc.Button(text_hd, id=f"id-{TAG}-button", **ARGS_BUTTON_SUBMIT)

    # define components
    form = dbc.Form(children=[
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

    # define variables
    if pathname == PATH_EMAIL_REGISTER_PWD:
        path_result = PATH_EMAIL_REGISTER_PWD_RESULT
    else:
        path_result = PATH_EMAIL_RESETPWD_PWD_RESULT

    # return result
    return None, True, path_result
