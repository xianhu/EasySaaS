# _*_ coding: utf-8 _*_

"""
template of sign page
"""

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from components import cbrand


def layout(pathname, search, tag, **kwargs):
    """
    layout of template
    """
    # define components
    src_image = dash.get_asset_url(kwargs["image_src"])
    left = html.Img(src=src_image, className="img-fluid")

    # define components
    kwargs_button = dict(size="lg", class_name="w-100 mt-4")
    right = html.Div(children=[
        html.Div(kwargs["text_hd"], className="text-center fs-1"),
        html.Div(kwargs["text_sub"], className="text-center text-muted"),

        html.Div(kwargs["form_items"], className="mt-4"),
        html.Div(id=f"id-{tag}-fb", className="text-danger text-center"),

        dbc.Button(kwargs["text_button"], id=f"id-{tag}-button", **kwargs_button),
        html.Div(kwargs["other_list"], className="d-flex justify-content-between"),
    ], className=None)

    # return result
    return dbc.Container(children=[
        cbrand.layout(class_name="position-absolute top-0 start-0 p-0"),
        dbc.Row(children=[
            dbc.Col(left, width=10, md={"size": 4, "offset": 0}, class_name="mt-auto mt-md-0"),
            dbc.Col(right, width=10, md={"size": 3, "offset": 1}, class_name="mb-auto mb-md-0"),
        ], align="center", justify="center", class_name="vh-100"),
        # define components
        html.A(id={"type": "id-address", "index": tag}),
        dcc.Store(id=f"id-{tag}-pathname", data=pathname),
        dcc.Store(id=f"id-{tag}-search", data=search),
    ], fluid=True, class_name=None)
