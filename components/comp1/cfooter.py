# _*_ coding: utf-8 _*_

"""
footer component
"""

import dash_bootstrap_components as dbc
from dash import html

from config import config_app_name
from utility import PATH_ROOT


def layout(fluid=None, class_name=None):
    """
    layout of component
    """
    # define components
    mhref = "mailto:service@databai.com"
    mservice = "Email: service@databai.com"
    addr = html.A(config_app_name, href=PATH_ROOT)

    # return result
    class_name = class_name or "small text-center border-top mt-auto py-2"
    return html.Footer(dbc.Container(dbc.Row(children=[
        dbc.Col(["Powered by ©2021 ", addr, ". All rights reserved."], width=12, md=6),
        dbc.Col(html.A(mservice, href=mhref, className="text-decoration-none"), width=12, md=6),
    ], class_name=None), fluid=fluid, class_name=None), className=class_name)
