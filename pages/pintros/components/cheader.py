# _*_ coding: utf-8 _*_

"""
header component
"""

import dash
import dash_bootstrap_components as dbc
from dash import html

HEADER = "Welcome to EasySaaS demo"
HEADERSUB = """
This project will be attempted to make a great starting point for your next big business as easy and efficent as possible. 
This project will create an easy way to build a SaaS application using Python and Dash.
""".strip()


def layout(pathname, search):
    """
    layout of component
    """
    # define components
    src = dash.get_asset_url("illustrations/intros.svg")
    image = html.Img(src=src, className="img-fluid")

    # define components
    intros = html.Div(children=[
        html.Div(HEADER, className="fs-1 text-center mb-2"),
        html.P(HEADERSUB, className="fs-5 text-center text-muted lead"),
    ])

    # return result
    return dbc.Row(children=[
        dbc.Col(image, width=10, md={"size": 5, "order": "last"}),
        dbc.Col(intros, width=10, md=5, class_name="mt-4 mt-md-0"),
    ], align="center", justify="around", class_name="mt-5")
