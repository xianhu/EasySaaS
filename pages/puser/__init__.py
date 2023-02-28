# _*_ coding: utf-8 _*_

"""
user page
"""

import logging
import urllib.parse

import flask_login
from dash import html

from .. import palert
from ..comps import header as comps_header

TAG = "user"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # check tab's name
    try:
        search = urllib.parse.parse_qs(search.lstrip("?").strip())
        assert search["tab"][0] in ("profile", "settings")
    except Exception as excep:
        logging.error("get tab failed: %s", excep)
        return palert.layout_500(pathname, search)
    tab = search["tab"][0]

    # return result
    return html.Div(children=[
        comps_header.get_component_header(user_title=user_title, dot=True),
        html.Div(children=[
            html.Span(f"[{tab}] coming soon..."),
        ], className="w-75 m-auto mt-4"),
    ], className="bg-main vh-100 overflow-auto")
