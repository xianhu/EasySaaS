# _*_ coding: utf-8 _*_

"""
footer of page
"""

from dash import html
import dash_bootstrap_components as dbc

from config import config_app_name


def layout(pathname, search, fluid=None, class_container=None, class_footer=None):
    """
    layout of component
    """
    # define components
    mhref = "mailto:service@databai.com"
    mservice = "Email: service@databai.com"
    addr = html.A(config_app_name, href="/")

    # return result
    class_footer = class_footer or "small text-center border-top mt-auto py-2"
    return html.Footer(dbc.Container(dbc.Row(children=[
        dbc.Col(["Powered by ©2021 ", addr, ". All rights reserved."], width=12, md=6),
        dbc.Col(html.A(mservice, href=mhref, className="text-decoration-none"), width=12, md=6),
    ], class_name="w-100 mx-auto"), fluid=fluid, class_name=class_container), className=class_footer)
