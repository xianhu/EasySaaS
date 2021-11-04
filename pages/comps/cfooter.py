# _*_ coding: utf-8 _*_

"""
footer of page
"""

import dash_bootstrap_components as dbc
from dash import html

from config import config_app_name


def layout(pathname, search, fluid=None):
    """
    layout of components
    """
    addr = html.A(config_app_name, href="/")
    mail_href = "mailto:service@databai.com"
    mail_service = "Email: service@databai.com"
    return html.Footer(dbc.Container(children=[
        html.Div(["Powered by ©2021 ", addr, ". All rights reserved."]),
        html.A(mail_service, href=mail_href, className="text-decoration-none")
    ], fluid=fluid), className="text-center small border-top py-4")
