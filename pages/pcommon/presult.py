# _*_ coding: utf-8 _*_

"""
page of result
"""

import flask

from ..comps import layout_salert
from ..consts import *
from . import palert


def layout(pathname, search):
    """
    layout of page
    """
    if pathname == PATH_REGISTER_EMAIL_RESULT or pathname == PATH_RESET_EMAIL_RESULT:
        email = flask.session.get("email", "")
        text_hd = "Sending success"
        text_sub = f"An email has sent to [{email}], go mailbox to verify it."
        return layout_salert(text_hd, text_sub, "Back to home", href=PATH_INDEX)

    if pathname == PATH_REGISTER_EMAIL_PWD_RESULT or pathname == PATH_RESET_EMAIL_PWD_RESULT:
        text_hd = "Setting success"
        text_sub = "The password was set successfully."
        return layout_salert(text_hd, text_sub, "Go to login", href=PATH_LOGIN)

    return palert.layout_404(pathname, search)
