# _*_ coding: utf-8 _*_

"""
page of register / login
"""

from . import pemail, plogin, ppwd, presult
from .consts import *


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_LOGIN or pathname == PATH_LOGOUT:
        content = plogin.layout(pathname, search)

    elif pathname == PATH_REGISTER_EMAIL or pathname == PATH_RESET_EMAIL:
        content = pemail.layout(pathname, search)
    elif pathname == PATH_REGISTER_EMAIL_RESULT or pathname == PATH_RESET_EMAIL_RESULT:
        content = presult.layout_email(pathname, search)

    elif pathname == PATH_REGISTER_EMAIL_PWD or pathname == PATH_RESET_EMAIL_PWD:
        content = ppwd.layout(pathname, search)
    elif pathname == PATH_REGISTER_EMAIL_PWD_RESULT or pathname == PATH_RESET_EMAIL_PWD_RESULT:
        content = presult.layout_pwd(pathname, search)

    # return result
    return [content, ]
