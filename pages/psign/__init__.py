# _*_ coding: utf-8 _*_

"""
page of register / login
"""

from ..paths import *
from . import pemail, plogin, ppwd, presult


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_LOGIN or pathname == PATH_LOGOUT:
        content = plogin.layout(pathname, search)

    elif pathname == PATH_EMAIL_REGISTER or pathname == PATH_EMAIL_RESETPWD:
        content = pemail.layout(pathname, search)
    elif pathname == PATH_EMAIL_REGISTER_RESULT or pathname == PATH_EMAIL_RESETPWD_RESULT:
        content = presult.layout_email(pathname, search)

    elif pathname == PATH_EMAIL_REGISTER_PWD or pathname == PATH_EMAIL_RESETPWD_PWD:
        content = ppwd.layout(pathname, search)
    elif pathname == PATH_EMAIL_REGISTER_PWD_RESULT or pathname == PATH_EMAIL_RESETPWD_PWD_RESULT:
        content = presult.layout_pwd(pathname, search)

    # return result
    return [content, ]
