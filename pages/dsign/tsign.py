# _*_ coding: utf-8 _*_

"""
template of sign page
"""

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html


def layout(pathname, search, tag, **kwargs):
    """
    layout of template
    """
    # define components
    src_image = dash.get_asset_url(kwargs.get("src_image"))
    col_left = fac.AntdCol(children=[
        fac.AntdImage(src=src_image, preview=False)
    ], span=20, md=dict(span=8, offset=0), className=None)

    # define components
    kwargs_button = dict(type="primary", size="large", autoSpin=True, className="w-100")
    col_right = fac.AntdCol(children=[
        html.Div(kwargs["text_title"], className="text-center fs-2"),
        html.Div(kwargs["text_subtitle"], className="text-center text-muted"),

        html.Div(kwargs["form_items"], className="mt-4"),
        fac.AntdButton(kwargs["text_button"], id=f"id-{tag}-button", **kwargs_button),

        html.Div(kwargs["other_list"], className="d-flex justify-content-between mt-1"),
    ], span=20, md=dict(span=6, offset=0), className=None)

    # return result
    return html.Div(children=[
        fuc.FefferyExecuteJs(id=f"id-{tag}-executejs"),
        dcc.Store(id=f"id-{tag}-data", data=kwargs["data"]),
        fac.AntdRow(children=[
            fac.AntdCol(span=1, className="vh-100"),
            col_left, col_right,
            fac.AntdCol(span=1, className="vh-100"),
        ], align="middle", justify="center", gutter=60),
    ], className=None)
