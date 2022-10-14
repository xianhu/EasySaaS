# _*_ coding: utf-8 _*_

"""
email page
"""

import hashlib
import json
import urllib.parse
import uuid

import dash
import dash_bootstrap_components as dbc
import flask
import flask_mail
from dash import Input, Output, State, html

from app import User, app_mail, app_redis
from config import config_app_domain, config_app_name
from utility.consts import RE_EMAIL
from utility.paths import PATH_ROOT, PATH_LOGIN, PATH_REGISTER, PATH_RESETPWD
from . import ERROR_EMAIL_FORMAT, ERROR_EMAIL_EXIST, ERROR_EMAIL_NOTEXIST
from . import FORGET_PWD_HD, FORGET_PWD_SUB, FORGET_PWD_BUTTON
from . import LABEL_EMAIL, LINK_SIGN_IN, LINK_SIGN_UP, LINK_FORGET_PWD
from . import SIGN_UP_HD, SIGN_UP_SUB, SIGN_UP_BUTTON
from . import tsign
from .. import palert

TAG = "email"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    form_items = dbc.Form(dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-email", type="email"),
        dbc.Label(f"{LABEL_EMAIL}:", html_for=f"id-{TAG}-email"),
    ]), class_name=None)

    # define args
    kwargs_temp = dict(
        src_image="illustrations/register.svg",
        text_hd=SIGN_UP_HD,
        text_sub=SIGN_UP_SUB,
        form_items=form_items,
        text_button=SIGN_UP_BUTTON,
        other_list=[
            html.A(LINK_SIGN_IN, href=PATH_LOGIN),
            html.A(LINK_FORGET_PWD, href=PATH_RESETPWD),
        ],
        data=pathname,
    ) if pathname == PATH_REGISTER else dict(
        src_image="illustrations/resetpwd.svg",
        text_hd=FORGET_PWD_HD,
        text_sub=FORGET_PWD_SUB,
        form_items=form_items,
        text_button=FORGET_PWD_BUTTON,
        other_list=[
            html.A(LINK_SIGN_IN, href=PATH_LOGIN),
            html.A(LINK_SIGN_UP, href=PATH_REGISTER),
        ],
        data=pathname,
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


def layout_result(pathname, search, **kwargs):
    """
    layout of page
    """
    return palert.layout(pathname, search, **dict(
        text_hd="Sending success",
        text_sub=f"An email has sent to {flask.session.get('email')}.",
        text_button="Back to home",
        return_href=PATH_ROOT,
    ))


@dash.callback([
    Output(f"id-{TAG}-feedback", "children"),
    Output({"type": "id-address", "index": TAG}, "href"),
], [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-email", "value"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pathname):
    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        return ERROR_EMAIL_FORMAT, dash.no_update
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = User.query.get(_id)
    if pathname == PATH_REGISTER and user:
        return ERROR_EMAIL_EXIST, dash.no_update
    if pathname == PATH_RESETPWD and (not user):
        return ERROR_EMAIL_NOTEXIST, dash.no_update

    # send email and cache
    if not app_redis.get(_id):
        token = str(uuid.uuid4())

        # define href of verify
        query_string = urllib.parse.urlencode(dict(_id=_id, token=token))
        href_verify = f"{config_app_domain}{pathname}-pwd?{query_string}"

        # send email
        if pathname == PATH_REGISTER:
            subject = f"Registration of {config_app_name}"
        else:
            subject = f"Resetting password of {config_app_name}"
        body = f"please click link in 10 minutes: {href_verify}"
        app_mail.send(flask_mail.Message(subject, body=body, recipients=[email, ]))

        # cache token and email
        app_redis.set(_id, json.dumps([token, email]), ex=60 * 10)

    # set session
    flask.session["email"] = email

    # return result
    return None, f"{pathname}/result"
