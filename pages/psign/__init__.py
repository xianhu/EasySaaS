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

    elif pathname == PATH_REGISTERE or pathname == PATH_RESETPWDE:
        content = pemail.layout(pathname, search)
    elif pathname == f"{PATH_REGISTERE}-result" or pathname == f"{PATH_RESETPWDE}-result":
        content = palert.layout_email(pathname, search, PATH_INTROS)

    elif pathname == f"{PATH_REGISTERE}-pwd" or pathname == f"{PATH_RESETPWDE}-pwd":
        content = ppwd.layout(pathname, search)
    elif pathname == f"{PATH_REGISTERE}-pwd-result" or pathname == f"{PATH_RESETPWDE}-pwd-result":
        content = palert.layout_password(pathname, search, PATH_LOGIN)

    # return result
    return [content, ]
