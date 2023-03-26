# _*_ coding: utf-8 _*_

"""
email[signup/forgotpwd] page
"""

import urllib.parse
import uuid

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
import flask
import flask_mail
from dash import Input, Output, State

from app import User, app_db, app_mail
from config import CONFIG_APP_NAME, CONFIG_APP_DOMAIN
from utility import get_md5
from utility.consts import RE_EMAIL, FMT_EXECUTEJS_HREF
from utility.paths import PATH_SIGNUP, PATH_FORGOTPWD
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

    # define kwargs
    kwargs_temp = dict(
        src_image="illustrations/signup.svg",
        text_title="Welcome to system",
        text_subtitle="Fill out the email to get started.",
        form_items=[form_email, row_cpc],
        data=PATH_SIGNUP,
    ) if pathname == PATH_SIGNUP else dict(
        src_image="illustrations/forgotpwd.svg",
        text_title="Forgot password?",
        text_subtitle="Fill out the email to reset password.",
        form_items=[form_email, row_cpc],
        data=PATH_FORGOTPWD,
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


def layout_result(pathname, search, **kwargs):
    """
    layout of page
    """
    email = flask.session.get("email")
    return palert.layout(pathname, search, status="success", **dict(
        text_title="Sending success",
        text_subtitle=f"An email has sent to {email}.",
        text_button="Now, go to mailbox!",
        return_href=None,
    ))


@dash.callback([dict(
    status=Output(f"id-{TAG}-form-email", "validateStatus"),
    help=Output(f"id-{TAG}-form-email", "help"),
), dict(
    status=Output(f"id-{TAG}-form-cpc", "validateStatus"),
    help=Output(f"id-{TAG}-form-cpc", "help"),
    refresh=Output(f"id-{TAG}-image-cpc", "refresh"),
), dict(
    button_loading=Output(f"id-{TAG}-button", "loading"),
    executejs_string=Output(f"id-{TAG}-executejs", "jsString"),
)], [
    Input(f"id-{TAG}-button", "nClicks"),
    State(f"id-{TAG}-input-email", "value"),
    State(f"id-{TAG}-input-cpc", "value"),
    State(f"id-{TAG}-image-cpc", "captcha"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, vcpc, vimage, pathname):
    # define outputs
    out_email = dict(status="", help="")
    out_cpc = dict(status="", help="", refresh=False)
    out_others = dict(button_loading=False, executejs_string=None)

    # check email
    email = (email or "").strip()
    if not RE_EMAIL.match(email):
        out_email["status"] = "error"
        out_email["help"] = "Format of email is invalid"
        # out_cpc["refresh"] = True if email else False
        return out_email, out_cpc, out_others

    # check captcha
    vcpc = (vcpc or "").strip()
    if (not vcpc) or (vcpc != vimage):
        out_cpc["status"] = "error"
        out_cpc["help"] = "Captcha is incorrect"
        out_cpc["refresh"] = True if vcpc else False
        return out_email, out_cpc, out_others

    # check user
    _id = get_md5(email)
    user = app_db.session.get(User, _id)
    if pathname == PATH_SIGNUP and (user and (user.status == 1)):
        out_email["status"] = "error"
        out_email["help"] = "This email has been registered"
        out_cpc["refresh"] = True
        return out_email, out_cpc, out_others
    if pathname == PATH_FORGOTPWD and ((not user) or (user.status != 1)):
        out_email["status"] = "error"
        out_email["help"] = "This email hasn't been registered"
        out_cpc["refresh"] = True
        return out_email, out_cpc, out_others

    # send email and add/update user ==============================================================
    token = user.token_verify if user and user.token_verify else str(uuid.uuid4())

    # define query and href of verify
    query = urllib.parse.urlencode(dict(_id=_id, token=token))
    href = f"{CONFIG_APP_DOMAIN.strip('/')}{pathname}-setpwd?{query}"

    # define subject and body
    if pathname == PATH_SIGNUP:
        subject = f"Registration of {CONFIG_APP_NAME}"
    else:
        subject = f"Resetting password of {CONFIG_APP_NAME}"
    mail_body = f"please click link: {href}"
    mail_html = f"please click link: <a href='{href}'>Verify the email</a>"

    # send email
    kwargs = dict(body=mail_body, html=mail_html)
    app_mail.send(flask_mail.Message(subject, **kwargs, recipients=[email, ]))

    # add/update user
    if not user:
        user = User(id=_id, email=email, token_verify=token, status=0)
        app_db.session.add(user)
        app_db.session.commit()
    else:
        user.token_verify = token
        # user.status = 0 !!!
        app_db.session.commit()
    # =============================================================================================

    # set session and go result
    flask.session["email"] = email
    out_others["executejs_string"] = FMT_EXECUTEJS_HREF.format(href=f"{pathname}/result")

    # return result
    return out_email, out_cpc, out_others
