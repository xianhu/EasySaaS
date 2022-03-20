# _*_ coding: utf-8 _*_

"""
template page
"""

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from config import config_app_name
from .paths import PATH_INTROS


def layout(pathname, search, tag, params):
    """
    layout of page
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
    return dbc.Container(children=[
        dbc.NavbarBrand(children=[
            html.Img(src=dash.get_asset_url("favicon.svg"), style={"width": "1.2rem"}),
            html.Span(config_app_name, className="fs-5 align-middle ms-1"),
        ], href=PATH_INTROS, class_name="position-absolute top-0 start-0 p-0"),

        dbc.Row(children=[
            dbc.Col(left, width=10, md={"size": 4, "offset": 0}, class_name="mt-auto mt-md-0"),
            dbc.Col(right, width=10, md={"size": 3, "offset": 1}, class_name="mb-auto mb-md-0"),
        ], align="center", justify="center", class_name="vh-100"),

        html.A(id={"type": "id-address", "index": tag}),
        dcc.Store(id=f"id-{tag}-pathname", data=pathname),
        dcc.Store(id=f"id-{tag}-search", data=search),
    ], fluid=None, class_name=None)
