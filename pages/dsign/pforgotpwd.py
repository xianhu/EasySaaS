# _*_ coding: utf-8 _*_

"""
forgotpwd page
"""

import json
import urllib.parse

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import Input, Output, State, dcc, html
from flask import session as flask_session

from core.consts import FMT_EXECUTEJS_HREF, RE_EMAIL
from core.security import create_access_token
from core.settings import settings
from models import DbMaker
from models.crud import crud_user
from tasks.email import send_email
from .. import palert
from ..comps import get_component_logo
from ..paths import *

TAG = "forgotpwd"

a_log_in = html.A("Log in", href=PATH_LOGIN)
a_sign_up = html.A("Sign up", href=PATH_SIGNUP)
a_forgot_pwd = html.A("Forgot password?", href=PATH_FORGOTPWD)


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    input_email = fac.AntdInput(id=f"id-{TAG}-input-email", placeholder="Email", size="large")
    form_email = fac.AntdFormItem(input_email, id=f"id-{TAG}-form-email", required=True)

    # define components
    input_cpc = fac.AntdInput(id=f"id-{TAG}-input-cpc", placeholder="Captcha", size="large")
    form_cpc = fac.AntdFormItem(input_cpc, id=f"id-{TAG}-form-cpc", required=True)

    # define components
    image_cpc = fuc.FefferyCaptcha(id=f"id-{TAG}-image-cpc", charNum=4)
    row_cpc = fac.AntdRow([fac.AntdCol(form_cpc, span=12), fac.AntdCol(image_cpc)], justify="space-between")

    # define components
    input_code = fac.AntdInput(id=f"id-{TAG}-input-code", placeholder="code", size="large")
    form_code = fac.AntdFormItem(input_code, id=f"id-{TAG}-form-code", required=True)

    # define components
    input_pwd1 = fac.AntdInput(id=f"id-{TAG}-input-pwd1", placeholder="Enter Password", size="large", mode="password")
    form_pwd1 = fac.AntdFormItem(input_pwd1, id=f"id-{TAG}-form-pwd1", required=True)
    input_pwd2 = fac.AntdInput(id=f"id-{TAG}-input-pwd2", placeholder="Confirm Password", size="large", mode="password")
    form_pwd2 = fac.AntdFormItem(input_pwd2, id=f"id-{TAG}-form-pwd2", required=True)

    # return result
    kwargs_button = dict(type="primary", size="large", block=True, autoSpin=True)
    return html.Div(children=[
        html.Div(get_component_logo(size=40), className="text-center mt-5 mb-4"),
        # define components
        fac.AntdRow(fac.AntdCol(html.Div(children=[
            html.Div("Forgot password?", className="text-center fs-3"),
            html.Div("Fill out the email to reset password.", className="text-center text-muted"),

            fac.AntdForm([form_email, row_cpc], className="mt-4"),
            fac.AntdButton("Send code", id=f"id-{TAG}-send", **kwargs_button),

            fac.AntdForm([form_code, form_pwd1, form_pwd2], className="mt-4"),
            fac.AntdButton("Update password", id=f"id-{TAG}-button", **kwargs_button),

            fac.AntdRow([a_log_in, a_sign_up], justify="space-between", className="mt-2"),
        ], className="bg-white shadow rounded p-4"), span=20, md=6), justify="center"),
        # define components
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
        dcc.Store(id=f"id-{TAG}-data", data=kwargs.get("nextpath") or PATH_ROOT),
    ], className="vh-100 overflow-auto")


def layout_result(pathname, search, **kwargs):
    """
    layout of page
    """
    email = flask_session.get("email")
    return palert.layout(pathname, search, status="success", **dict(
        text_title="Sending success",
        text_subtitle=f"An email has sent to {email}.",
        text_button="Now, go to mailbox!",
        return_href=PATH_ROOT,
    ))


@dash.callback([dict(
    status=Output(f"id-{TAG}-form-email", "validateStatus"),
    help=Output(f"id-{TAG}-form-email", "help"),
), dict(
    status=Output(f"id-{TAG}-form-cpc", "validateStatus"),
    help=Output(f"id-{TAG}-form-cpc", "help"),
), dict(
    status=Output(f"id-{TAG}-form-terms", "validateStatus"),
    help=Output(f"id-{TAG}-form-terms", "help"),
), dict(
    cpc_refresh=Output(f"id-{TAG}-image-cpc", "refresh"),
    button_loading=Output(f"id-{TAG}-button", "loading"),
    executejs_string=Output(f"id-{TAG}-executejs", "jsString"),
)], [
    Input(f"id-{TAG}-button", "nClicks"),
    State(f"id-{TAG}-input-email", "value"),
    State(f"id-{TAG}-input-cpc", "value"),
    State(f"id-{TAG}-image-cpc", "captcha"),
    State(f"id-{TAG}-checkbox-terms", "checked"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, vcpc, vimage, checked, pathname):
    # define outputs
    out_email = dict(status="", help="")
    out_cpc = dict(status="", help="")
    out_terms = dict(status="", help="")
    out_others = dict(cpc_refresh=False, button_loading=False, executejs_string=None)

    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        out_email["status"] = "error"
        out_email["help"] = "Format of email is invalid"
        return out_email, out_cpc, out_terms, out_others

    # check captcha
    vcpc = (vcpc or "").strip()
    if (not vcpc) or (vcpc != vimage):
        out_cpc["status"] = "error"
        out_cpc["help"] = "Captcha is incorrect"
        out_others["cpc_refresh"] = True if vcpc else False
        return out_email, out_cpc, out_terms, out_others

    # check terms if signup
    if pathname == PATH_SIGNUP and (not checked):
        out_terms["status"] = "error"
        out_terms["help"] = "Please agree to terms of use and privacy policy"
        return out_email, out_cpc, out_terms, out_others

    # get user from db
    with DbMaker() as db:
        user_db = crud_user.get_by_email(db, email=email)

    # check user
    if pathname == PATH_SIGNUP and (user_db and user_db.status == 1):
        out_email["status"] = "error"
        out_email["help"] = "This email has been registered"
        out_others["cpc_refresh"] = True if vcpc else False
        return out_email, out_cpc, out_terms, out_others
    if pathname == PATH_FORGOTPWD and (not (user_db and user_db.status == 1)):
        out_email["status"] = "error"
        out_email["help"] = "This email hasn't been registered"
        out_others["cpc_refresh"] = True if vcpc else False
        return out_email, out_cpc, out_terms, out_others

    # send email ==================================================================================
    sub = json.dumps(dict(email=email, type="sign"))
    token = create_access_token(sub=sub, expires_duration=60 * 10)

    # define mail_subject
    if pathname == PATH_SIGNUP:
        mail_subject = "Registration of {{ app_name }}"
    else:
        mail_subject = "Resetting password of {{ app_name }}"

    # define href and mail_html
    href = urllib.parse.urljoin(settings.APP_DOMAIN, f"{pathname}-setpwd?token={token}")
    mail_html = "please click link: <a href='{{ href }}'>Verify the email</a>"

    # send email
    render = dict(app_name=settings.APP_NAME, href=href)
    send_email(to=email, subject=mail_subject, html=mail_html, render=render)
    # =============================================================================================

    # set session and go result
    flask_session["email"] = email
    out_others["executejs_string"] = FMT_EXECUTEJS_HREF.format(href=f"{pathname}/result")

    # return result
    return out_email, out_cpc, out_terms, out_others
