# _*_ coding: utf-8 _*_

"""
layout of header
"""

import dash_bootstrap_components as dbc
from dash import html

HEADER = "Welcome to EasySaaS live demo"
DESC = """
This project will be attempt to make a great starting point 
for your next big business as easy and efficent as possible. 
This project will create an easy way to build a SaaS application using Python and Dash.
"""


def layout(pathname, search):
    return html.Div(children=[
        dbc.Row(dbc.Col(HEADER, class_name="fs-1 fw-bold text-center"), justify="center"),
        dbc.Row(dbc.Col(DESC, width=10, md=6, class_name="text-center"), justify="center"),
    ], className="bg-primary bg-opacity-25 py-5")
