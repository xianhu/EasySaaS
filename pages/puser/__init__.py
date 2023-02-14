# _*_ coding: utf-8 _*_

"""
user page
"""

import flask_login
from dash import html

from ..comps import header as comps_header

TAG = "user"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    current_user = flask_login.current_user
    user_title = current_user.email.split("@")[0]

    # return result
    return html.Div(children=[
        comps_header.get_component_header(None, user_title, dot=True),
        html.Div(children=[
            html.Span("coming soon"), html.Br(),
            html.A("back to home", href="/"),
        ], className="w-75 m-auto mt-4"),
    ], className="bg-main vh-100 overflow-auto")
