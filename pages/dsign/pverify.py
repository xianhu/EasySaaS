# _*_ coding: utf-8 _*_

"""
verify page
"""

from flask import session as flask_session

from core.security import get_access_sub
from .. import palert

TAG = "verify"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    if not search.get("token"):
        return palert.layout_expired(pathname, search)

    # check token
    token = search.get("token")[0]
    if not get_access_sub(token):
        return palert.layout_expired(pathname, search)

    # login and return
    flask_session["token"] = token
    return palert.layout_verify_success(pathname, search)