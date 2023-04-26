# _*_ coding: utf-8 _*_

"""
signup page
"""

import json
import urllib.parse

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import Input, Output, State, dcc, html
from flask import session as flask_session

from core.consts import FMT_EXECUTEJS_HREF, RE_EMAIL, RE_PWD
from core.security import create_token, get_password_hash
from core.settings import settings
from models import DbMaker
from models.crud import crud_user
from models.schemas import UserCreate
from tasks.email import send_email
from ..comps import get_component_logo
from ..paths import *

TAG = "signup"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    input_email = fac.AntdInput(id=f"id-{TAG}-input-email", placeholder="Email", size="large")
    form_email = fac.AntdFormItem(input_email, id=f"id-{TAG}-form-email", required=True)

    # define components
    input_pwd1 = fac.AntdInput(id=f"id-{TAG}-input-pwd1", placeholder="Enter Password", size="large", mode="password")
    form_pwd1 = fac.AntdFormItem(input_pwd1, id=f"id-{TAG}-form-pwd1", required=True)

    input_pwd2 = fac.AntdInput(id=f"id-{TAG}-input-pwd2", placeholder="Confirm Password", size="large", mode="password")
    form_pwd2 = fac.AntdFormItem(input_pwd2, id=f"id-{TAG}-form-pwd2", required=True)

    # define components
    input_cpc = fac.AntdInput(id=f"id-{TAG}-input-cpc", placeholder="Captcha", size="large")
    form_cpc = fac.AntdFormItem(input_cpc, id=f"id-{TAG}-form-cpc", required=True)

    image_cpc = fuc.FefferyCaptcha(id=f"id-{TAG}-image-cpc", charNum=4)
    row_cpc = fac.AntdRow([fac.AntdCol(form_cpc, span=12), fac.AntdCol(image_cpc)], justify="space-between")

    # define components
    checkbox_terms = fac.AntdCheckbox(id=f"id-{TAG}-checkbox-terms")
    span_terms = html.Span(children=[
        "I agree to ", html.A("terms of use", href="#"),
        " and ", html.A("privacy policy", href="#"), ".",
    ], className="text-muted ms-2")
    form_terms = fac.AntdFormItem([checkbox_terms, span_terms], id=f"id-{TAG}-form-terms")

    # return result
    next_path = kwargs.get("next_path") or PATH_ROOT
    kwargs_button = dict(type="primary", size="large", block=True, autoSpin=True)
    return html.Div(children=[
        html.Div(get_component_logo(size=40), className="text-center mt-5 mb-4"),
        # define components
        fac.AntdRow(fac.AntdCol(html.Div(children=[
            html.Div("Welcome to system", className="text-center fs-3"),
            html.Div("Fill out the email to get started.", className="text-center text-muted"),

            fac.AntdForm([form_email, form_pwd1, form_pwd2, row_cpc, form_terms], className="mt-4"),
            fac.AntdButton("Sign up", id=f"id-{TAG}-button", **kwargs_button),

            fac.AntdRow(children=[
                html.A("Log in", href=PATH_LOGIN),
                html.A("Forgot password?", href=PATH_FORGOTPWD),
            ], justify="space-between", className="mt-2"),
        ], className="bg-white shadow rounded p-4"), span=20, md=6), justify="center"),
        # define components
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
        dcc.Store(id=f"id-{TAG}-data", data=next_path),
    ], className="vh-100 overflow-auto")


@dash.callback([dict(
    status=Output(f"id-{TAG}-form-email", "validateStatus"),
    help=Output(f"id-{TAG}-form-email", "help"),
), dict(
    status1=Output(f"id-{TAG}-form-pwd1", "validateStatus"),
    help1=Output(f"id-{TAG}-form-pwd1", "help"),
    status2=Output(f"id-{TAG}-form-pwd2", "validateStatus"),
    help2=Output(f"id-{TAG}-form-pwd2", "help"),
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
    State(f"id-{TAG}-input-pwd1", "value"),
    State(f"id-{TAG}-input-pwd2", "value"),
    State(f"id-{TAG}-input-cpc", "value"),
    State(f"id-{TAG}-image-cpc", "captcha"),
    State(f"id-{TAG}-checkbox-terms", "checked"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd1, pwd2, cpc, image, checked, next_path):
    # define outputs
    out_email = dict(status="", help="")
    out_pwd = dict(status1="", help1="", status2="", help2="")
    out_cpc = dict(status="", help="")
    out_terms = dict(status="", help="")
    out_others = dict(cpc_refresh=False, button_loading=False, executejs_string=None)

    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        out_email["status"] = "error"
        out_email["help"] = "Format of email is invalid"
        return out_email, out_pwd, out_cpc, out_terms, out_others

    # check password
    pwd1 = (pwd1 or "").strip()
    pwd2 = (pwd2 or "").strip()
    if (not pwd1) or (len(pwd1) < 6):
        out_pwd["status1"] = "error"
        out_pwd["help1"] = "Password is too short"
        return out_email, out_pwd, out_cpc, out_terms, out_others
    if not RE_PWD.match(pwd1):
        out_pwd["status1"] = "error"
        out_pwd["help1"] = "Password must contain numbers and letters"
        return out_email, out_pwd, out_cpc, out_terms, out_others
    if (not pwd2) or (pwd2 != pwd1):
        out_pwd["status2"] = "error"
        out_pwd["help2"] = "Passwords are inconsistent"
        return out_email, out_pwd, out_cpc, out_terms, out_others
    pwd_hash = get_password_hash(pwd1)

    # check terms
    if not checked:
        out_terms["status"] = "error"
        out_terms["help"] = "Please agree to terms of use and privacy policy"
        return out_email, out_pwd, out_cpc, out_terms, out_others

    # check captcha
    cpc = (cpc or "").strip()
    if (not cpc) or (cpc != image):
        out_cpc["status"] = "error"
        out_cpc["help"] = "Captcha is incorrect"
        out_others["cpc_refresh"] = True if cpc else False
        return out_email, out_pwd, out_cpc, out_terms, out_others

    # get user from db
    with DbMaker() as db:
        user_db = crud_user.get_by_email(db, email=email)

        # check user
        if user_db and (user_db.status is not None):
            out_email["status"] = "error"
            out_email["help"] = "This email has been registered"
            out_others["cpc_refresh"] = True if cpc else False
            return out_email, out_pwd, out_cpc, out_terms, out_others

        # create user and login user
        user_schema = UserCreate(pwd=pwd_hash, email=email)
        user_db = crud_user.create(db, obj_schema=user_schema)
        flask_session["token_access"] = create_token(user_db.id)

        # send email ==============================================================================
        sub = json.dumps(dict(email=email, type="verify"))
        token = create_token(sub=sub, expires_duration=60 * 10)
        href = urllib.parse.urljoin(settings.APP_DOMAIN, f"{PATH_VERIFY}?token={token}")

        # define mail_subject and mail_html
        mail_subject = "Welcome to {{ app_name }}"
        mail_html = "please click link: <a href='{{ href }}'>Verify the email</a>"

        # send email
        render = dict(app_name=settings.APP_NAME, href=href)
        send_email(to=email, subject=mail_subject, html=mail_html, render=render)
        # =========================================================================================
    out_others["executejs_string"] = FMT_EXECUTEJS_HREF.format(href=next_path)

    # return result
    return out_email, out_pwd, out_cpc, out_terms, out_others
