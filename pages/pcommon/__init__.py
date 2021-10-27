# _*_ coding: utf-8 _*_

"""
common page
"""

from . import palert, pemail, plogin, ppwd, presult
from ..consts import *


def layout(pathname, search):
    """
    layout of page
    """
    if pathname == PATH_LOGIN or pathname == PATH_LOGOUT:
        return plogin.layout(pathname, search)

    if pathname == PATH_REGISTER_EMAIL or pathname == PATH_RESET_EMAIL:
        return pemail.layout(pathname, search)

    if pathname == PATH_REGISTER_EMAIL_RESULT or pathname == PATH_RESET_EMAIL_RESULT:
        return presult.layout(pathname, search)

    if pathname == PATH_REGISTER_EMAIL_PWD or pathname == PATH_RESET_EMAIL_PWD:
        return ppwd.layout(pathname, search)

    if pathname == PATH_REGISTER_EMAIL_PWD_RESULT or pathname == PATH_RESET_EMAIL_PWD_RESULT:
        return presult.layout(pathname, search)

    # return result
    return palert.layout_404(pathname, search)
