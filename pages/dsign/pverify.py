# _*_ coding: utf-8 _*_

"""
verify page
"""

import json
import logging

from flask import session as flask_session

from core.security import create_access_token, get_access_sub
from models import DbMaker
from models.crud import crud_user
from .. import palert

TAG = "verify"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # check search
    if not search.get("token"):
        return palert.layout_expired(pathname, search)
    token = search.get("token")[0]

    # check token
    try:
        sub = json.loads(get_access_sub(token))
        assert sub["type"] == "verify", "token type error"
    except Exception as excep:
        logging.error(excep)
        return palert.layout_expired(pathname, search)
    email = sub.get("email")

    # get user from db
    with DbMaker() as db:
        user_db = crud_user.get_by_email(db, email=email)
        user_db.email_verified = True
        user_db = crud_user.update(db, obj_db=user_db)

    # login and return
    flask_session["token"] = create_access_token(user_db.id)
    return palert.layout_verify_success(pathname, search)
