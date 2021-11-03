# _*_ coding: utf-8 _*_

"""
page of notify
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search):
    """
    layout of page
    """
    return html.Div(children=[
        dbc.Alert("This is a primary alert", color="primary", class_name="w-75"),
        dbc.Alert("This is a secondary alert", color="secondary", class_name="w-75"),
        dbc.Alert("This is a success alert! Well done!", color="success", class_name="w-75"),
        dbc.Alert("This is a warning alert... be careful...", color="warning", class_name="w-75"),
        dbc.Alert("This is a danger alert. Scary!", color="danger", class_name="w-75"),
        dbc.Alert("This is an info alert. Good to know!", color="info", class_name="w-75"),
        dbc.Alert("This is a dark alert", color="dark", class_name="w-75"),
    ], className="d-flex flex-column align-items-center w-100 py-4 h-100 overflow-scroll")
