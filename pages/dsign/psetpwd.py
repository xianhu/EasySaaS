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
from utility.consts import RE_PWD, FMT_EXECUTEJS_HREF
from utility.paths import PATH_LOGIN, PATH_ROOT
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
        return palert.layout_expired(pathname, search, return_href=PATH_ROOT)

    # define components
    email_input = fac.AntdInput(id=f"id-{TAG}-email", value=email, size="large", readOnly=True)
    email_form = fac.AntdFormItem(email_input, id=f"id-{TAG}-email-form", required=True)

    # define components
    pwd1_input = fac.AntdInput(id=f"id-{TAG}-pwd1", placeholder="Password", size="large", mode="password")
    pwd1_form = fac.AntdFormItem(pwd1_input, id=f"id-{TAG}-pwd1-form", required=True)
    pwd2_input = fac.AntdInput(id=f"id-{TAG}-pwd2", placeholder="Password", size="large", mode="password")
    pwd2_form = fac.AntdFormItem(pwd2_input, id=f"id-{TAG}-pwd2-form", required=True)

    # define kwargs
    kwargs_temp = dict(
        src_image="illustrations/setpwd.svg",
        text_title="Set password",
        text_subtitle="Set the password of this email please.",
        form_items=fac.AntdForm([email_form, pwd1_form, pwd2_form]),
        text_button="Set password",
        other_list=[None, None],
        data=pathname,
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
    pwd1_status=Output(f"id-{TAG}-pwd1-form", "validateStatus"),
    pwd1_help=Output(f"id-{TAG}-pwd1-form", "help"),
    pwd2_status=Output(f"id-{TAG}-pwd2-form", "validateStatus"),
    pwd2_help=Output(f"id-{TAG}-pwd2-form", "help"),
), dict(
    button_loading=Output(f"id-{TAG}-button", "loading"),
    js_string=Output(f"id-{TAG}-executejs", "jsString"),
)], [
    Input(f"id-{TAG}-button", "nClicks"),
    State(f"id-{TAG}-email", "value"),
    State(f"id-{TAG}-pwd1", "value"),
    State(f"id-{TAG}-pwd2", "value"),
    State(f"id-{TAG}-data", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, email, pwd1, pwd2, pathname):
    # define outputs
    out_status_help = dict(
        pwd1_status="", pwd1_help="",
        pwd2_status="", pwd2_help="",
    )
    out_others = dict(button_loading=False, js_string=None)

    # check password
    if (not pwd1) or (len(pwd1) < 6):
        out_status_help["pwd1_status"] = "error"
        out_status_help["pwd1_help"] = "Password is too short"
        return out_status_help, out_others
    if not RE_PWD.match(pwd1):
        out_status_help["pwd1_status"] = "error"
        out_status_help["pwd1_help"] = "Password must contain numbers and letters"
        return out_status_help, out_others
    if (not pwd2) or (pwd2 != pwd1):
        out_status_help["pwd2_status"] = "error"
        out_status_help["pwd2_help"] = "Passwords are inconsistent"
        return out_status_help, out_others
    pwd = User.get_password_hash(pwd1)

    # check user
    _id = User.get_id_by_email(email)
    user = app_db.session.query(User).get(_id)
    if user:
        user.pwd = pwd
    else:
        user = User(id=_id, pwd=pwd, email=email)

    # commit user
    app_db.session.merge(user)
    app_db.session.commit()

    # delete cache
    app_redis.delete(_id)
    out_others["js_string"] = FMT_EXECUTEJS_HREF.format(href=f"{pathname}/result")

    # return result
    return out_status_help, out_others
