# _*_ coding: utf-8 _*_

"""
email[signup/reset] page
"""

import json

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import Input, Output, State, dcc, html
from flask import session as flask_session

from core.consts import FMT_EXECUTEJS_HREF, RE_EMAIL, RE_PWD
from core.settings import error_tips
from core.utils import security, utemail
from models import DbMaker
from models.crud import crud_user
from models.schemas import UserCreate, UserUpdate
from ..comps import get_component_logo
from ..paths import *

TAG = "email"


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

    image_cpc = fuc.FefferyCaptcha(id=f"id-{TAG}-image-cpc", charNum=4)
    row_cpc = fac.AntdRow([fac.AntdCol(form_cpc, span=12), fac.AntdCol(image_cpc)], justify="space-between")

    # define components
    input_code = fac.AntdInput(id=f"id-{TAG}-input-code", placeholder="Verify code", size="large")
    form_code = fac.AntdFormItem(input_code, id=f"id-{TAG}-form-code", required=True)

    # define components
    input_pwd1 = fac.AntdInput(id=f"id-{TAG}-input-pwd1", placeholder="Enter Password", size="large", mode="password")
    form_pwd1 = fac.AntdFormItem(input_pwd1, id=f"id-{TAG}-form-pwd1", required=True)

    input_pwd2 = fac.AntdInput(id=f"id-{TAG}-input-pwd2", placeholder="Confirm Password", size="large", mode="password")
    form_pwd2 = fac.AntdFormItem(input_pwd2, id=f"id-{TAG}-form-pwd2", required=True)

    # define text according to pathname
    if pathname == PATH_SIGNUP:
        text_title = "Welcome to system"
        text_subtitle = "Fill out the email to get started."
        text_button = "Sign up"
    else:
        text_title = "Reset password"
        text_subtitle = "Fill out the email to reset password."
        text_button = "Reset password"
    text_send = "Send code"

    # return result
    kwargs_button = dict(type="primary", size="large", block=True, autoSpin=True)
    return html.Div(children=[
        html.Div(get_component_logo(size=40), className="text-center mt-5 mb-4"),
        # define components
        fac.AntdRow(fac.AntdCol(html.Div(children=[
            html.Div(text_title, className="text-center fs-3"),
            html.Div(text_subtitle, className="text-center text-muted"),

            fac.AntdForm([form_email, row_cpc], className="mt-4"),
            fac.AntdButton(text_send, id=f"id-{TAG}-send", **kwargs_button),

            fac.AntdForm([form_code, form_pwd1, form_pwd2], className="mt-4"),
            fac.AntdButton(text_button, id=f"id-{TAG}-button", **kwargs_button),
        ], className="bg-white shadow rounded p-4"), span=20, md=6), justify="center"),
        # define components
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
        dcc.Store(id=f"id-{TAG}-data", data=pathname),
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
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, cpc, image, pathname):
    # define outputs
    out_email = dict(status="", help="")
    out_cpc = dict(status="", help="")
    out_others = dict(cpc_refresh=False, button_loading=False, button_disabled=False)

    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        out_email["status"] = "error"
        out_email["help"] = error_tips.EMAIL_INVALID
        return out_email, out_cpc, out_others

    # check captcha
    cpc = (cpc or "").strip()
    if (not cpc) or (cpc != image):
        out_cpc["status"] = "error"
        out_cpc["help"] = error_tips.CAPTCHA_INCORRECT
        out_others["cpc_refresh"] = True if cpc else False
        return out_email, out_cpc, out_others

    # get user from db
    with DbMaker() as db:
        user_db = crud_user.get_by_email(db, email=email)

    # check user -- existed
    if pathname == PATH_SIGNUP and (user_db and user_db.status is not None):
        out_email["status"] = "error"
        out_email["help"] = error_tips.EMAIL_EXISTED
        out_others["cpc_refresh"] = True if cpc else False
        return out_email, out_cpc, out_others

    # check user -- not existed
    if pathname == PATH_RESET and (not (user_db and user_db.status == 1)):
        out_email["status"] = "error"
        out_email["help"] = error_tips.EMAIL_NOT_EXISTED
        out_others["cpc_refresh"] = True if cpc else False
        return out_email, out_cpc, out_others

    # create token_verify with code, and send email
    token_verify = utemail.send_email_code(email, _type=pathname)
    flask_session["token_verify"] = token_verify if token_verify else ""

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
def _button_click(n_clicks, code, pwd1, pwd2, pathname):
    # define outputs
    out_code = dict(status="", help="")
    out_pwd = dict(status1="", help1="", status2="", help2="")
    out_others = dict(button_loading=False, executejs_string=None)

    # parse token_verify from session
    token_verify = flask_session.get("token_verify", "")
    sub_dict = json.loads(security.get_token_sub(token_verify) or "{}")

    # check token_verify
    if (not sub_dict.get("code")) or (not sub_dict.get("email")):
        out_code["status"] = "error"
        out_code["help"] = error_tips.CODE_INVALID
        return out_code, out_pwd, out_others

    # check code
    code = (code or "").strip()
    code_token = str(sub_dict["code"])
    if (not code) or (code_token != code):
        out_code["status"] = "error"
        out_code["help"] = error_tips.CODE_INVALID
        return out_code, out_pwd, out_others

    # check password
    pwd1 = (pwd1 or "").strip()
    pwd2 = (pwd2 or "").strip()
    if (not pwd1) or (len(pwd1) < 6):
        out_pwd["status1"] = "error"
        out_pwd["help1"] = error_tips.PWD_FMT_SHORT
        return out_code, out_pwd, out_others
    if not RE_PWD.match(pwd1):
        out_pwd["status1"] = "error"
        out_pwd["help1"] = error_tips.PWD_FMT_ERROR
        return out_code, out_pwd, out_others
    if (not pwd2) or (pwd2 != pwd1):
        out_pwd["status2"] = "error"
        out_pwd["help2"] = error_tips.PWD_FMT_INCONSISTENT
        return out_code, out_pwd, out_others
    pwd_hash = security.get_pwd_hash(pwd1)

    # get user from db
    with DbMaker() as db:
        email = sub_dict.get("email")
        user_db = crud_user.get_by_email(db, email=email)
        if pathname == PATH_SIGNUP and (not user_db):
            # create user with email (verify)
            user_schema = UserCreate(pwd=pwd_hash, email=email, email_verify=True)
            crud_user.create(db, obj_schema=user_schema)
        if pathname == PATH_RESET and user_db:
            # update user's password
            user_schema = UserUpdate(pwd=pwd_hash)
            crud_user.update(db, obj_db=user_db, obj_schema=user_schema)

    # go next_path: login
    out_others["executejs_string"] = FMT_EXECUTEJS_HREF.format(href=PATH_LOGIN)

    # return result
    return out_code, out_pwd, out_others
