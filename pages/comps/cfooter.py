# _*_ coding: utf-8 _*_

"""
footer of page
"""

import dash_bootstrap_components as dbc
from dash import html

from config import config_app_name


def layout(pathname, search):
    """
    layout of components
    """
    mail_href = "mailto:service@databai.com"
    mail_service = "Email:service@databai.com"
    return dbc.Row(children=[
        dbc.Col("©2021 DataBai, Inc.", width=10, md=3),
        dbc.Col(html.A(config_app_name, href="/", className="fw-bold"), width=10, md=3),
        dbc.Col(html.A(mail_service, href=mail_href, className="text-decoration-none"), width=10, md=3),
    ], justify="around", class_name="text-center border-top w-100 p-3")
