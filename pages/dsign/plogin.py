# _*_ coding: utf-8 _*_

"""
login page
"""

import hashlib

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
import flask_login
from dash import Input, Output, State, html
from werkzeug import security

from app import UserLogin, app_db
from utility.consts import RE_EMAIL, FMT_EXECUTEJS_HREF
from utility.paths import PATH_ROOT, PATH_SIGNUP, PATH_FORGOTPWD
from . import tsign

TAG = "login"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    email_input = fac.AntdInput(id=f"id-{TAG}-email", placeholder="Email", size="large")
    email_form = fac.AntdFormItem(email_input, id=f"id-{TAG}-email-form", required=True)

    # define components
    pwd_input = fac.AntdInput(id=f"id-{TAG}-pwd", placeholder="Password", size="large", mode="password", passwordUseMd5=True)
    pwd_form = fac.AntdFormItem(pwd_input, id=f"id-{TAG}-pwd-form", required=True)

    # define components
    cpc_input = fac.AntdInput(id=f"id-{TAG}-cpc", placeholder="Captcha", size="large")
    cpc_form = fac.AntdFormItem(cpc_input, id=f"id-{TAG}-cpc-form", required=True)
    cpc_image = fuc.FefferyCaptcha(id=f"id-{TAG}-cpc-image", charNum=4)
    cpc_row = fac.AntdRow([fac.AntdCol(cpc_form, span=12), fac.AntdCol(cpc_image, span=12)], gutter=30)

    # define args
    kwargs_temp = dict(
        src_image="illustrations/login.svg",
        text_title="Welcome back",
        text_subtitle="Login to analysis your data.",
        form_items=fac.AntdForm([email_form, pwd_form, cpc_row]),
        text_button="Log in",
        other_list=[
            html.A("Sign up", href=PATH_SIGNUP),
            html.A("Forgot password?", href=PATH_FORGOTPWD),
        ],
        data=kwargs.get("nextpath") or PATH_ROOT,
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


@dash.callback([
    dict(
        email_status=Output(f"id-{TAG}-email-form", "validateStatus"),
        email_help=Output(f"id-{TAG}-email-form", "help"),
        pwd_status=Output(f"id-{TAG}-pwd-form", "validateStatus"),
        pwd_help=Output(f"id-{TAG}-pwd-form", "help"),
        cpc_status=Output(f"id-{TAG}-cpc-form", "validateStatus"),
        cpc_help=Output(f"id-{TAG}-cpc-form", "help"),
    ),
    dict(
        cpc_refresh=Output(f"id-{TAG}-cpc-image", "refresh"),
        button_loading=Output(f"id-{TAG}-button", "loading"),
        js_string=Output(f"id-{TAG}-executejs", "jsString"),
    ),
], [
    Input(f"id-{TAG}-button", "nClicks"),
    State(f"id-{TAG}-email", "value"),
    State(f"id-{TAG}-pwd", "md5Value"),
    State(f"id-{TAG}-cpc", "value"),
    State(f"id-{TAG}-cpc-image", "captcha"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd_md5, cinput, vimage, nextpath):
    # define outputs
    out_status_help = dict(
        email_status=None, email_help=None,
        pwd_status=None, pwd_help=None,
        cpc_status=None, cpc_help=None,
    )
    out_others = dict(cpc_refresh=False, button_loading=False, js_string=None)

    # check captcha
    if (cinput != vimage) or (not cinput):
        out_status_help["cpc_status"] = "error"
        out_status_help["cpc_help"] = "Captcha is incorrect"
        return out_status_help, out_others

    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        out_status_help["email_status"] = "error"
        out_status_help["email_help"] = "Format of email is invalid"
        return out_status_help, out_others
    _id = hashlib.md5(email.encode()).hexdigest()

    # check user
    user = app_db.session.query(UserLogin).get(_id)
    if not user:
        out_status_help["email_status"] = "error"
        out_status_help["email_help"] = "This Email does't exist"
        return out_status_help, out_others

    # check password
    if not security.check_password_hash(user.pwd, pwd_md5 or ""):
        out_status_help["pwd_status"] = "error"
        out_status_help["pwd_help"] = "Password is incorrect"
        return out_status_help, out_others

    # login user
    flask_login.login_user(user, remember=True)

    # return result
    out_others["js_string"] = FMT_EXECUTEJS_HREF.format(href=nextpath)
    return out_status_help, out_others
