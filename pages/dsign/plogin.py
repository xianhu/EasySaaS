# _*_ coding: utf-8 _*_

"""
login page
"""

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
import flask_login
from dash import Input, Output, State

from app import UserLogin
from core.consts import FMT_EXECUTEJS_HREF, RE_EMAIL
from core.paths import PATH_ROOT
from core.security import check_password_hash
from models import get_session
from . import tsign

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

    # define components
    image_cpc = fuc.FefferyCaptcha(id=f"id-{TAG}-image-cpc", charNum=4)
    row_cpc = fac.AntdRow([fac.AntdCol(form_cpc, span=12), fac.AntdCol(image_cpc)], justify="space-between")

    # define kwargs
    kwargs_temp = dict(
        text_title="Welcome back",
        text_subtitle="Login to analysis your models.",
        form_items=[form_email, form_pwd, row_cpc],
        data=kwargs.get("nextpath") or PATH_ROOT,
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


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
def _button_click(n_clicks, email, pwd, vcpc, vimage, nextpath):
    # define outputs
    out_email = dict(status="", help="")
    out_pwd = dict(status="", help="")
    out_cpc = dict(status="", help="")
    out_others = dict(cpc_refresh=False, button_loading=False, executejs_string=None)

    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        out_email["status"] = "error"
        out_email["help"] = "Format of email is invalid"
        return out_email, out_pwd, out_cpc, out_others

    # check captcha
    vcpc = (vcpc or "").strip()
    if (not vcpc) or (vcpc != vimage):
        out_cpc["status"] = "error"
        out_cpc["help"] = "Captcha is incorrect"
        out_others["cpc_refresh"] = True if vcpc else False
        return out_email, out_pwd, out_cpc, out_others

    # check user
    for session in get_session():
        user = session.query(UserLogin).filter(
            UserLogin.email == email,
        ).first()
    if not (user and user.status == 1):
        out_email["status"] = "error"
        out_email["help"] = "This email hasn't been registered"
        out_others["cpc_refresh"] = True if vcpc else False
        return out_email, out_pwd, out_cpc, out_others

    # check password
    pwd = (pwd or "").strip()
    if not check_password_hash(pwd, user.pwd):
        out_pwd["status"] = "error"
        out_pwd["help"] = "Password is incorrect"
        out_others["cpc_refresh"] = True if vcpc else False
        return out_email, out_pwd, out_cpc, out_others

    # login user and go nextpath
    flask_login.login_user(user, remember=True)
    out_others["executejs_string"] = FMT_EXECUTEJS_HREF.format(href=nextpath)

    # return result
    return out_email, out_pwd, out_cpc, out_others
