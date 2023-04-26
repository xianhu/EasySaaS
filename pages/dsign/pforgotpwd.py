# _*_ coding: utf-8 _*_

"""
forgotpwd page
"""

import json
import random

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import Input, Output, State, dcc, html
from flask import session as flask_session

from core.consts import FMT_EXECUTEJS_HREF, RE_EMAIL, RE_PWD
from core.security import create_access_token, get_access_sub, get_password_hash
from core.settings import settings
from models import DbMaker
from models.crud import crud_user
from tasks.email import send_email
from ..comps import get_component_logo
from ..paths import *

TAG = "forgotpwd"


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
    next_path = kwargs.get("next_path") or PATH_ROOT
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
        ], className="bg-white shadow rounded p-4"), span=20, md=6), justify="center"),
        # define components
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
        dcc.Store(id=f"id-{TAG}-data", data=next_path),
    ], className="vh-100 overflow-auto")


@dash.callback([dict(
    status=Output(f"id-{TAG}-form-email", "validateStatus"),
    help=Output(f"id-{TAG}-form-email", "help"),
), dict(
    status=Output(f"id-{TAG}-form-cpc", "validateStatus"),
    help=Output(f"id-{TAG}-form-cpc", "help"),
), dict(
    cpc_refresh=Output(f"id-{TAG}-image-cpc", "refresh"),
    button_loading=Output(f"id-{TAG}-send", "loading"),
    button_disabled=Output(f"id-{TAG}-send", "disabled"),
)], [
    Input(f"id-{TAG}-send", "nClicks"),
    State(f"id-{TAG}-input-email", "value"),
    State(f"id-{TAG}-input-cpc", "value"),
    State(f"id-{TAG}-image-cpc", "captcha"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, cpc, image):
    # define outputs
    out_email = dict(status="", help="")
    out_cpc = dict(status="", help="")
    out_others = dict(cpc_refresh=False, button_loading=False, button_disabled=False)

    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        out_email["status"] = "error"
        out_email["help"] = "Format of email is invalid"
        return out_email, out_cpc, out_others

    # check captcha
    cpc = (cpc or "").strip()
    if (not cpc) or (cpc != image):
        out_cpc["status"] = "error"
        out_cpc["help"] = "Captcha is incorrect"
        out_others["cpc_refresh"] = True if cpc else False
        return out_email, out_cpc, out_others

    # get user from db
    with DbMaker() as db:
        user_db = crud_user.get_by_email(db, email=email)

        # check user
        if not (user_db and user_db.status == 1):
            out_email["status"] = "error"
            out_email["help"] = "This email hasn't been registered"
            out_others["cpc_refresh"] = True if cpc else False
            return out_email, out_cpc, out_others

        # create code and save to token_reset
        code = random.randint(100001, 999999)
        sub = json.dumps(dict(email=email, code=code, type="reset"))
        flask_session["token_reset"] = create_access_token(sub, expires_duration=60 * 10)

        # send email ==============================================================================
        mail_subject = "Code of {{ app_name }}"
        mail_html = "Code of {{ app_name }}: <b>{{ code }}</b>"

        # send email
        render = dict(app_name=settings.APP_NAME, code=code)
        send_email(to=email, subject=mail_subject, html=mail_html, render=render)
        # =========================================================================================

    # return result
    out_others["button_disabled"] = True
    return out_email, out_cpc, out_others


@dash.callback([dict(
    status=Output(f"id-{TAG}-form-code", "validateStatus"),
    help=Output(f"id-{TAG}-form-code", "help"),
), dict(
    status1=Output(f"id-{TAG}-form-pwd1", "validateStatus"),
    help1=Output(f"id-{TAG}-form-pwd1", "help"),
    status2=Output(f"id-{TAG}-form-pwd2", "validateStatus"),
    help2=Output(f"id-{TAG}-form-pwd2", "help"),
), dict(
    button_loading=Output(f"id-{TAG}-button", "loading"),
    executejs_string=Output(f"id-{TAG}-executejs", "jsString"),
)], [
    Input(f"id-{TAG}-button", "nClicks"),
    State(f"id-{TAG}-input-code", "value"),
    State(f"id-{TAG}-input-pwd1", "value"),
    State(f"id-{TAG}-input-pwd2", "value"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, code, pwd1, pwd2, next_path):
    # define outputs
    out_code = dict(status="", help="")
    out_pwd = dict(status1="", help1="", status2="", help2="")
    out_others = dict(button_loading=False, executejs_string=None)

    # check code
    code = (code or "").strip()
    if not code:
        out_code["status"] = "error"
        out_code["help"] = "Code is required"
        return out_code, out_pwd, out_others
    code = int(code)

    # check code
    sub = get_access_sub(flask_session.get("token_reset", ""))
    sub_dict = json.loads(sub or "{}")
    if (not sub_dict) or (sub_dict.get("code") != code):
        out_code["status"] = "error"
        out_code["help"] = "Code is incorrect"
        return out_code, out_pwd, out_others
    email = sub_dict.get("email")

    # check password
    pwd1 = (pwd1 or "").strip()
    pwd2 = (pwd2 or "").strip()
    if (not pwd1) or (len(pwd1) < 6):
        out_pwd["status1"] = "error"
        out_pwd["help1"] = "Password is too short"
        return out_code, out_pwd, out_others
    if not RE_PWD.match(pwd1):
        out_pwd["status1"] = "error"
        out_pwd["help1"] = "Password must contain numbers and letters"
        return out_code, out_pwd, out_others
    if (not pwd2) or (pwd2 != pwd1):
        out_pwd["status2"] = "error"
        out_pwd["help2"] = "Passwords are inconsistent"
        return out_code, out_pwd, out_others
    pwd_hash = get_password_hash(pwd1)

    # get user from db
    with DbMaker() as db:
        user_db = crud_user.get_by_email(db, email=email)
        user_db.pwd = pwd_hash
        user_db = crud_user.update(db, obj_db=user_db)
    out_others["executejs_string"] = FMT_EXECUTEJS_HREF.format(href=next_path)

    # return result
    return out_code, out_pwd, out_others
