# _*_ coding: utf-8 _*_

"""
email[signup/forgotpwd] page
"""

import urllib.parse

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import Input, Output, State, html
from flask import session as flask_session

from app import User
from core.consts import FMT_EXECUTEJS_HREF, RE_EMAIL
from core.paths import PATH_FORGOTPWD, PATH_ROOT, PATH_SIGNUP
from core.security import create_access_token
from core.settings import settings
from . import tsign
from .. import palert

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

    # define components
    image_cpc = fuc.FefferyCaptcha(id=f"id-{TAG}-image-cpc", charNum=4)
    row_cpc = fac.AntdRow([fac.AntdCol(form_cpc, span=12), fac.AntdCol(image_cpc)], justify="space-between")

    # define components
    checkbox_terms = fac.AntdCheckbox(id=f"id-{TAG}-checkbox-terms")
    span_terms = html.Span(children=[
        "I agree to ", html.A("terms of use", href="#"),
        " and ", html.A("privacy policy", href="#"), ".",
    ], className="text-muted ms-2")

    # define components (d-none if signup)
    class_terms = "" if pathname == PATH_SIGNUP else "d-none"
    form_terms = fac.AntdFormItem([checkbox_terms, span_terms], id=f"id-{TAG}-form-terms", className=class_terms)

    # define kwargs
    kwargs_temp = dict(
        text_title="Welcome to system",
        text_subtitle="Fill out the email to get started.",
        form_items=[form_email, row_cpc, form_terms],
        data=PATH_SIGNUP,
    ) if pathname == PATH_SIGNUP else dict(
        text_title="Forgot password?",
        text_subtitle="Fill out the email to reset password.",
        form_items=[form_email, row_cpc, form_terms],
        data=PATH_FORGOTPWD,
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


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

    # check user
    user = app_db.session.query(User).filter(User.email == email).first()
    if pathname == PATH_SIGNUP and (user and (user.status == 1)):
        out_email["status"] = "error"
        out_email["help"] = "This email has been registered"
        out_others["cpc_refresh"] = True if vcpc else False
        return out_email, out_cpc, out_terms, out_others
    if pathname == PATH_FORGOTPWD and (not (user and user.status == 1)):
        out_email["status"] = "error"
        out_email["help"] = "This email hasn't been registered"
        out_others["cpc_refresh"] = True if vcpc else False
        return out_email, out_cpc, out_terms, out_others

    # send email ==================================================================================
    token = create_access_token(subject=email, expires_duration=60 * 10)
    link_verify = urllib.parse.urljoin(settings.APP_DOMAIN, f"{pathname}-setpwd?token={token}")

    # define subject and body
    if pathname == PATH_SIGNUP:
        subject = f"Registration of {settings.APP_NAME}"
    else:
        subject = f"Resetting password of {settings.APP_NAME}"
    mail_body = f"please click link: {link_verify}"
    mail_html = f"please click link: <a href='{link_verify}'>Verify the email</a>"

    # send email
    kwargs = dict(body=mail_body, html=mail_html)
    # app_mail.send(flask_mail.Message(subject, **kwargs, recipients=[email, ]))
    # =============================================================================================

    # set session and go result
    flask_session["email"] = email
    out_others["executejs_string"] = FMT_EXECUTEJS_HREF.format(href=f"{pathname}/result")

    # return result
    return out_email, out_cpc, out_terms, out_others
