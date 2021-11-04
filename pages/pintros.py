# _*_ coding: utf-8 _*_

"""
intros page
"""

import dash_bootstrap_components as dbc
from dash import html

from config import config_src_intros

from .comps import cfooter, cnavbar, cpricing
from .paths import *

HEADER = "Welcome to EasySaaS demo"
DESC = """
This project will be attempt to make a great starting point 
for your next big business as easy and efficent as possible. 
This project will create an easy way to build a SaaS application using Python and Dash.
"""


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    navbar = cnavbar.layout(pathname, search)
    footer = cfooter.layout(pathname, search)

    # define components
    image = html.Img(src=config_src_intros, className="img-fluid")
    content = dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(image, width=10, md={"size": 5, "order": 2}),
            dbc.Col(children=[
                html.Div(HEADER, className="fs-1 text-center mb-2"),
                html.Div(DESC, className="fs-5 text-center text-muted lead"),
            ], width=10, md={"size": 5, "order": 1}, class_name="mt-4 mt-md-0"),
        ], align="center", justify="around", className="w-100 py-4"),
        cpricing.layout(pathname, search),
    ])

    # return result
    return [navbar, content, footer]
