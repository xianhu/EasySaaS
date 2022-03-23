# _*_ coding: utf-8 _*_

"""
template of sign page
"""

import dash
import dash_bootstrap_components as dbc
from dash import html

from components import cbrand
from templates import tnormal


def layout(pathname, search, tag, params):
    """
    layout of template
    """
    # define components
    left = html.Img(src=dash.get_asset_url(params["image_src"]), className="img-fluid")

    # define components
    args_button = {"size": "lg", "class_name": "w-100 mt-4"}
    right = html.Div([
        html.Div(params["text_hd"], className="text-center fs-1"),
        html.Div(params["text_sub"], className="text-center text-muted"),

        html.Div(params["form_items"], className="mt-4"),
        html.Div(id=f"id-{tag}-fb", className="text-danger text-center"),

        dbc.Button(params["text_button"], id=f"id-{tag}-button", **args_button),
        html.Div(params["other_list"], className="d-flex justify-content-between"),
    ])

    # return result
    return tnormal.layout(pathname, search, tag, children=dbc.Container(children=[
        cbrand.layout(pathname, search, class_name="position-absolute top-0 start-0 p-0"),
        dbc.Row(children=[
            dbc.Col(left, width=10, md={"size": 4, "offset": 0}, class_name="mt-auto mt-md-0"),
            dbc.Col(right, width=10, md={"size": 3, "offset": 1}, class_name="mb-auto mb-md-0"),
        ], align="center", justify="center", class_name="vh-100"),
    ], fluid=None), class_name=None)
