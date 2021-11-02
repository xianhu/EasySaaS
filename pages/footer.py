# _*_ coding: utf-8 _*_

"""
layout of footer
"""

import dash_bootstrap_components as dbc
from dash import html

from config import config_app_name


def layout_footer(pathname, search):
    mail_href = "mailto:service@databai.com"
    mail_service = "Email:service@databai.com"

    # return result
    return dbc.Row(children=[
        dbc.Col("©2021 DataBai, Inc.", width=10, md=3, lg=3),
        dbc.Col(html.A(config_app_name, href="/", className="fw-bold"), width=10, md=3, lg=3),
        dbc.Col(html.A(mail_service, href=mail_href, className="text-decoration-none"), width=10, md=3, lg=3),
    ], justify="around", class_name="gx-0 text-center border-top mt-auto p-3")
