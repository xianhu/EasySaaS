# _*_ coding: utf-8 _*_

"""
set password page
"""

import json
import logging
import urllib.parse

import dash
import feffery_antd_components as fac
from dash import Input, Output, State

from app import User, app_db, app_redis
from utility import get_md5
from utility.consts import RE_PWD, FMT_EXECUTEJS_HREF
from utility.paths import PATH_LOGIN
from . import tsign
from .. import palert

TAG = "setpwd"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    try:
        # get values from search
        search = urllib.parse.parse_qs(search.lstrip("?").strip())
        _id, _token = search.get("_id")[0], search.get("token")[0]

        # get values from redis
        token, email = json.loads(app_redis.get(_id))

        # verify token values
        assert token == _token, (token, _token)
    except Exception as excep:
        logging.error("token expired or error: %s", excep)
        return palert.layout_expired(pathname, search)

    # define components
    input_email = fac.AntdInput(id=f"id-{TAG}-input-email", value=email, size="large", readOnly=True)
    form_email = fac.AntdFormItem(input_email, id=f"id-{TAG}-form-email", required=True)

    # define components
    input_pwd1 = fac.AntdInput(id=f"id-{TAG}-input-pwd1", placeholder="Enter Password", size="large", mode="password")
    form_pwd1 = fac.AntdFormItem(input_pwd1, id=f"id-{TAG}-form-pwd1", required=True)
    input_pwd2 = fac.AntdInput(id=f"id-{TAG}-input-pwd2", placeholder="Confirm Password", size="large", mode="password")
    form_pwd2 = fac.AntdFormItem(input_pwd2, id=f"id-{TAG}-form-pwd2", required=True)

    # define kwargs
    kwargs_temp = dict(
        src_image="illustrations/setpwd.svg",
        text_title="Set password",
        text_subtitle="Set the password of this email.",
        form_items=[form_email, form_pwd1, form_pwd2],
        data=[pathname, email],
    )

    # return result
    return tsign.layout(pathname, search, TAG, **kwargs_temp)


def layout_result(pathname, search, **kwargs):
    """
    layout of page
    """
    return palert.layout(pathname, search, status="success", **dict(
        text_title="Setting success",
        text_subtitle="The password was set successfully.",
        text_button="Go to login",
        return_href=PATH_LOGIN,
    ))


@dash.callback([dict(
    status1=Output(f"id-{TAG}-form-pwd1", "validateStatus"),
    help1=Output(f"id-{TAG}-form-pwd1", "help"),
    status2=Output(f"id-{TAG}-form-pwd2", "validateStatus"),
    help2=Output(f"id-{TAG}-form-pwd2", "help"),
), dict(
    button_loading=Output(f"id-{TAG}-button", "loading"),
    executejs_string=Output(f"id-{TAG}-executejs", "jsString"),
)], [
    Input(f"id-{TAG}-button", "nClicks"),
    State(f"id-{TAG}-input-email", "value"),
    State(f"id-{TAG}-input-pwd1", "value"),
    State(f"id-{TAG}-input-pwd2", "value"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd1, pwd2, pathname_email):
    # define outputs
    out_pwd = dict(status1="", help1="", status2="", help2="")
    out_others = dict(button_loading=False, executejs_string=None)

    # check email
    pathname, email_tmp = pathname_email
    if email != email_tmp:
        return out_pwd, out_others

    # check password
    pwd1 = (pwd1 or "").strip()
    pwd2 = (pwd2 or "").strip()
    if (not pwd1) or (len(pwd1) < 6):
        out_pwd["status1"] = "error"
        out_pwd["help1"] = "Password is too short"
        return out_pwd, out_others
    if not RE_PWD.match(pwd1):
        out_pwd["status1"] = "error"
        out_pwd["help1"] = "Password must contain numbers and letters"
        return out_pwd, out_others
    if (not pwd2) or (pwd2 != pwd1):
        out_pwd["status2"] = "error"
        out_pwd["help2"] = "Passwords are inconsistent"
        return out_pwd, out_others

    # check user
    _id = get_md5(email)
    user = app_db.session.query(User).get(_id)
    if not user:
        user = User(id=_id, email=email)
    user.set_password_hash(pwd1)

    # commit user
    app_db.session.merge(user)
    app_db.session.commit()

    # delete cache
    app_redis.delete(_id)
    out_others["executejs_string"] = FMT_EXECUTEJS_HREF.format(href=f"{pathname}/result")

    # return result
    return out_pwd, out_others
