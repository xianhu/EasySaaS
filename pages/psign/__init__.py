# _*_ coding: utf-8 _*_

"""
sign page
"""

import flask

from ..palert import *
from ..paths import *
from . import pemail, plogin, ppwd


def layout(pathname, search):
    """
    layout of page
    """
    if pathname == PATH_LOGIN or pathname == PATH_LOGOUT:
        return plogin.layout(pathname, search)

    if pathname == PATH_REGISTERE or pathname == PATH_RESETPWDE:
        return pemail.layout(pathname, search)
    if pathname == f"{PATH_REGISTERE}-result" or pathname == f"{PATH_RESETPWDE}-result":
        email = flask.session.get("email", "")
        text_hd = "Sending success"
        text_sub = f"An email has sent to [{email}], go mailbox to verify it."
        return layout_simple(text_hd, text_sub, "Back to home", PATH_INTROS)

    if pathname == f"{PATH_REGISTERE}-pwd" or pathname == f"{PATH_RESETPWDE}-pwd":
        return ppwd.layout(pathname, search)
    if pathname == f"{PATH_REGISTERE}-pwd-result" or pathname == f"{PATH_RESETPWDE}-pwd-result":
        text_hd = "Setting success"
        text_sub = "The password was set successfully."
        return layout_simple(text_hd, text_sub, "Go to login", PATH_LOGIN)

    # return result
    return layout_404(pathname, search)
