# _*_ coding: utf-8 _*_

"""
sign page
"""

from .. import palert
from ..paths import *
from . import pemail, plogin, ppwd


def layout(pathname, search):
    """
    layout of page
    """
    content = None
    if pathname == PATH_LOGIN or pathname == PATH_LOGOUT:
        content = plogin.layout(pathname, search)

    elif pathname == PATH_REGISTER_E or pathname == PATH_RESETPWD_E:
        content = pemail.layout(pathname, search)
    elif pathname == f"{PATH_REGISTER_E}/result" or pathname == f"{PATH_RESETPWD_E}/result":
        content = palert.layout_email(pathname, search, PATH_INTROS)

    elif pathname == f"{PATH_REGISTER_E}/pwd" or pathname == f"{PATH_RESETPWD_E}/pwd":
        content = ppwd.layout(pathname, search)
    elif pathname == f"{PATH_REGISTER_E}/pwd/result" or pathname == f"{PATH_RESETPWD_E}/pwd/result":
        content = palert.layout_password(pathname, search, PATH_LOGIN)

    # return result
    return [content, ]
