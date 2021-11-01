# _*_ coding: utf-8 _*_

"""
page of result
"""

import flask

from ..common import *
from ..paths import *


def layout_email(pathname, search):
    """
    layout of page
    """
    email = flask.session.get("email", "")
    text_hd = "Sending success"
    text_sub = f"An email has sent to [{email}], go mailbox to verify it."
    return layout_salert(text_hd, text_sub, "Back to home", PATH_INTROS)


def layout_pwd(pathname, search):
    """
    layout of page
    """
    text_hd = "Setting success"
    text_sub = "The password was set successfully."
    return layout_salert(text_hd, text_sub, "Go to login", PATH_LOGIN)
