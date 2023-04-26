# _*_ coding: utf-8 _*_

"""
verify page
"""

import json
import logging

from flask import session as flask_session

from core.security import get_access_sub
from models import DbMaker
from models.crud import crud_user
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
    try:
        payload = json.loads(get_access_sub(token))
    except Exception as excep:
        logging.error(excep)
        return palert.layout_expired(pathname, search)
    email = payload.get("email")

    # update email_verify
    with DbMaker() as db:
        crud_user.update_email_verify(db, email=email)

        # login and return
        flask_session["token"] = token
        return palert.layout_verify_success(pathname, search)
