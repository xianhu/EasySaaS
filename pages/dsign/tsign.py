# _*_ coding: utf-8 _*_

"""
template of sign page
"""

import dash
import dash_bootstrap_components as dbc
import feffery_utils_components as fuc
from dash import dcc, html


def layout(pathname, search, tag, **kwargs):
    """
    layout of template
    """
    # define components
    src_image = kwargs["src_image"]
    col_left = dbc.Col(children=[
        html.Img(src=dash.get_asset_url(src_image), className="img-fluid")
    ], width=10, md={"size": 4, "offset": 0}, class_name="mt-auto mt-md-0")

    # define components
    kwargs_button = dict(size="lg", class_name="w-100 mt-4")
    col_right = dbc.Col(children=[
        html.Div(kwargs["text_hd"], className="text-center fs-2"),
        html.Div(kwargs["text_sub"], className="text-center text-muted"),

        html.Div(kwargs["form_items"], className="mt-4"),
        html.Div(id=f"id-{tag}-feedback", className="text-center text-danger"),

        dbc.Button(kwargs["text_button"], id=f"id-{tag}-button", **kwargs_button),
        html.Div(kwargs["other_list"], className="d-flex justify-content-between"),
    ], width=10, md={"size": 3, "offset": 1}, class_name="mb-auto mb-md-0")

    # return result
    return dbc.Container(children=[
        fuc.FefferyExecuteJs(id=f"id-{tag}-executejs"),
        dcc.Store(id=f"id-{tag}-data", data=kwargs["data"]),
        dbc.Row([col_left, col_right], align="center", justify="center", class_name="vh-100"),
    ], fluid=True, class_name="vh-100")
