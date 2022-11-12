# _*_ coding: utf-8 _*_

"""
email[signup/forgotpwd] page
"""

import hashlib
import json
import urllib.parse
import uuid

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
import flask
import flask_mail
from dash import Input, Output, State, html

from app import UserLogin, app_db, app_mail, app_redis
from config import config_app_domain, config_app_name
from utility.consts import RE_EMAIL, FMT_EXECUTEJS_HREF
from utility.paths import PATH_LOGIN, PATH_SIGNUP, PATH_FORGOTPWD
from . import tsign
from .. import palert

TAG = "email"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    email_input = fac.AntdInput(id=f"id-{TAG}-email", placeholder="Email", size="large")
    email_form = fac.AntdFormItem(email_input, id=f"id-{TAG}-email-form", required=True)

    # define components
    cpc_input = fac.AntdInput(id=f"id-{TAG}-cpc", placeholder="Captcha", size="large")
    cpc_form = fac.AntdFormItem(cpc_input, id=f"id-{TAG}-cpc-form", required=True)
    cpc_image = fuc.FefferyCaptcha(id=f"id-{TAG}-cpc-image", charNum=4)
    cpc_row = fac.AntdRow([fac.AntdCol(cpc_form, span=12), fac.AntdCol(cpc_image, span=12)], gutter=30)

    # define args
    kwargs_temp = dict(
        src_image="illustrations/signup.svg",
        text_title="Welcome to ES",
        text_subtitle="Fill out the email to get started.",
        form_items=fac.AntdForm([email_form, cpc_row]),
        text_button="Verify the email",
        other_list=[
            html.A("Log in", href=PATH_LOGIN),
            html.A("Forgot password?", href=PATH_FORGOTPWD),
        ],
        data=PATH_SIGNUP,
    ) if pathname == PATH_SIGNUP else dict(
        src_image="illustrations/forgotpwd.svg",
        text_title="Forgot password?",
        text_subtitle="Fill out the email to reset password.",
        form_items=fac.AntdForm([email_form, cpc_row]),
        text_button="Verify the email",
        other_list=[
            html.A("Log in", href=PATH_LOGIN),
            html.A("Sign up", href=PATH_SIGNUP),
        ],
        data=PATH_FORGOTPWD,
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


def layout_result(pathname, search, **kwargs):
    """
    layout of page
    """
    email = flask.session.get("email")
    return palert.layout(pathname, search, **dict(
        status="success",
        text_title="Sending success",
        text_subtitle=f"An email has sent to {email}.",
        text_button="Now, go to mailbox!",
        return_href=None,
    ))


@dash.callback([dict(
    email_status=Output(f"id-{TAG}-email-form", "validateStatus"),
    email_help=Output(f"id-{TAG}-email-form", "help"),
    cpc_status=Output(f"id-{TAG}-cpc-form", "validateStatus"),
    cpc_help=Output(f"id-{TAG}-cpc-form", "help"),
), dict(
    cpc_refresh=Output(f"id-{TAG}-cpc-image", "refresh"),
    button_loading=Output(f"id-{TAG}-button", "loading"),
    js_string=Output(f"id-{TAG}-executejs", "jsString"),
)], [
    Input(f"id-{TAG}-button", "nClicks"),
    State(f"id-{TAG}-email", "value"),
    State(f"id-{TAG}-cpc", "value"),
    State(f"id-{TAG}-cpc-image", "captcha"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, vcpc, vimage, pathname):
    # define outputs
    out_status_help = dict(
        email_status="", email_help="",
        cpc_status="", cpc_help="",
    )
    out_others = dict(cpc_refresh=False, button_loading=False, js_string=None)

    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        out_status_help["email_status"] = "error"
        out_status_help["email_help"] = "Format of email is invalid"
        return out_status_help, out_others

    # check captcha
    if (vcpc != vimage) or (not vcpc):
        out_status_help["cpc_status"] = "error"
        out_status_help["cpc_help"] = "Captcha is incorrect"
        out_others["cpc_refresh"] = True
        return out_status_help, out_others

    # check user
    _id = hashlib.md5(email.encode()).hexdigest()
    user = app_db.session.query(UserLogin).get(_id)
    if pathname == PATH_SIGNUP and user:
        out_status_help["email_status"] = "error"
        out_status_help["email_help"] = "This email has been registered"
        out_others["cpc_refresh"] = True
        return out_status_help, out_others
    if pathname == PATH_FORGOTPWD and (not user):
        out_status_help["email_status"] = "error"
        out_status_help["email_help"] = "This email hasn't been registered"
        out_others["cpc_refresh"] = True
        return out_status_help, out_others

    # send email and cache
    if not app_redis.get(_id):
        token = str(uuid.uuid4())

        # define href of verify
        query_string = urllib.parse.urlencode(dict(_id=_id, token=token))
        href_verify = f"{config_app_domain}{pathname}-setpwd?{query_string}"

        # send email
        if pathname == PATH_SIGNUP:
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
    out_others["js_string"] = FMT_EXECUTEJS_HREF.format(href=f"{pathname}/result")
    return out_status_help, out_others
