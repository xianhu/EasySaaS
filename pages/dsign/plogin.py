# _*_ coding: utf-8 _*_

"""
login page
"""

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import Input, Output, State, dcc, html
from flask import session as flask_session

from core.consts import FMT_EXECUTEJS_HREF, RE_EMAIL
from core.settings import error_tips
from core.utils.security import check_pwd_hash, create_token
from models import DbMaker
from models.crud import crud_user
from ..comps import get_component_logo
from ..paths import *

TAG = "login"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    input_email = fac.AntdInput(id=f"id-{TAG}-input-email", placeholder="Email", size="large")
    form_email = fac.AntdFormItem(input_email, id=f"id-{TAG}-form-email", required=True)

    # define components
    input_pwd = fac.AntdInput(id=f"id-{TAG}-input-pwd", placeholder="Password", size="large", mode="password")
    form_pwd = fac.AntdFormItem(input_pwd, id=f"id-{TAG}-form-pwd", required=True)

    # define components
    input_cpc = fac.AntdInput(id=f"id-{TAG}-input-cpc", placeholder="Captcha", size="large")
    form_cpc = fac.AntdFormItem(input_cpc, id=f"id-{TAG}-form-cpc", required=True)

    image_cpc = fuc.FefferyCaptcha(id=f"id-{TAG}-image-cpc", charNum=4)
    row_cpc = fac.AntdRow([fac.AntdCol(form_cpc, span=12), fac.AntdCol(image_cpc)], justify="space-between")

    # return result
    kwargs_button = dict(type="primary", size="large", block=True, autoSpin=True)
    return html.Div(children=[
        html.Div(get_component_logo(size=40), className="text-center mt-5 mb-4"),
        # define components
        fac.AntdRow(fac.AntdCol(html.Div(children=[
            html.Div("Welcome back", className="text-center fs-3"),
            html.Div("Login to analysis your models.", className="text-center text-muted"),

            fac.AntdForm([form_email, form_pwd, row_cpc], className="mt-4"),
            fac.AntdButton("Log in", id=f"id-{TAG}-button", **kwargs_button),

            fac.AntdRow(children=[
                html.A("Sign up", href=PATH_SIGNUP),
                html.A("Reset password", href=PATH_RESET),
            ], align="center", justify="space-between", className="mt-2"),
        ], className="bg-white shadow rounded p-4"), span=20, md=6), justify="center"),
        # define components
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs", jsString=None),
        dcc.Store(id=f"id-{TAG}-data", data=kwargs.get("next_path") or PATH_ROOT),
    ], className="vh-100 overflow-auto")


@dash.callback([dict(
    status=Output(f"id-{TAG}-form-email", "validateStatus"),
    help=Output(f"id-{TAG}-form-email", "help"),
), dict(
    status=Output(f"id-{TAG}-form-pwd", "validateStatus"),
    help=Output(f"id-{TAG}-form-pwd", "help"),
), dict(
    status=Output(f"id-{TAG}-form-cpc", "validateStatus"),
    help=Output(f"id-{TAG}-form-cpc", "help"),
), dict(
    cpc_refresh=Output(f"id-{TAG}-image-cpc", "refresh"),
    button_loading=Output(f"id-{TAG}-button", "loading"),
    executejs_string=Output(f"id-{TAG}-executejs", "jsString"),
)], [
    Input(f"id-{TAG}-button", "nClicks"),
    State(f"id-{TAG}-input-email", "value"),
    State(f"id-{TAG}-input-pwd", "value"),
    State(f"id-{TAG}-input-cpc", "value"),
    State(f"id-{TAG}-image-cpc", "captcha"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd, cpc, image, next_path):
    # define outputs
    out_email = dict(status="", help="")
    out_pwd = dict(status="", help="")
    out_cpc = dict(status="", help="")
    out_others = dict(cpc_refresh=False, button_loading=False, executejs_string=None)

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

    # check user
    if not (user_db and user_db.status == 1):
        out_email["status"] = "error"
        out_email["help"] = error_tips.EMAIL_NOT_EXISTED
        out_others["cpc_refresh"] = True if cpc else False
        return out_email, out_pwd, out_cpc, out_others

    # check password
    pwd_plain = (pwd or "").strip()
    if not check_pwd_hash(pwd_plain, user_db.pwd):
        out_pwd["status"] = "error"
        out_pwd["help"] = error_tips.PWD_INCORRECT
        out_others["cpc_refresh"] = True if cpc else False
        return out_email, out_pwd, out_cpc, out_others

    # login user and go next_path
    flask_session["token_access"] = create_token(user_db.id)
    out_others["executejs_string"] = FMT_EXECUTEJS_HREF.format(href=next_path)

    # return result
    return out_email, out_pwd, out_cpc, out_others
