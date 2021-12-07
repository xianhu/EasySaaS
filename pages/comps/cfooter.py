# _*_ coding: utf-8 _*_

"""
footer of page
"""

import dash_bootstrap_components as dbc
from dash import html

from config import config_app_name


def layout(pathname, search, fluid=None, class_container=None, class_footer=None):
    """
    layout of components
    """
    # define components
    addr = html.A(config_app_name, href="/")
    mail_href = "mailto:service@databai.com"
    mail_service = "Email: service@databai.com"

    # return result
    class_footer = class_footer or "small text-center border-top mt-auto py-2"
    return html.Footer(dbc.Container(dbc.Row(children=[
        dbc.Col(["Powered by ©2021 ", addr, ". All rights reserved."], width=12, md=6),
        dbc.Col(html.A(mail_service, href=mail_href, className="text-decoration-none"), width=12, md=6),
    ], class_name="w-100 mx-auto"), fluid=fluid, class_name=class_container), className=class_footer)
