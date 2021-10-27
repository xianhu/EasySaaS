# _*_ coding: utf-8 _*_

"""
footer of page
"""

import logging

import dash_bootstrap_components as dbc
from dash import html

from config import config_app_name
from .consts import *


def layout_footer(pathname, search):
    """
    layout of footer
    """
    logging.warning("pathname=%s, search=%s", pathname, search)
    assert (pathname in PATH_SET_INDEX) or (pathname in PATH_SET_SYSTEM)

    # define variables
    mail_href = "mailto:service@databai.com"
    mail_service = "Email:service@databai.com"
    href_brand = PATH_INDEX if pathname in PATH_SET_INDEX else PATH_SYSTEM

    # return result
    return dbc.Row(children=[
        dbc.Col("©2021 DataBai, Inc.", width=10, md=3, lg=3),
        dbc.Col(html.A(config_app_name, href=href_brand, className="fw-bold"), width=10, md=3, lg=3),
        dbc.Col(html.A(mail_service, href=mail_href, className="text-decoration-none"), width=10, md=3, lg=3),
    ], justify="around", class_name="gx-0 text-center w-100 position-absolute bottom-0 border-top p-3")
