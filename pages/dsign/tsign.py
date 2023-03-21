# _*_ coding: utf-8 _*_

"""
template of sign page
"""

import dash
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html

from utility.paths import PATH_LOGIN, PATH_SIGNUP, PATH_FORGOTPWD


def layout(pathname, search, tag, **kwargs):
    """
    layout of template
    """
    # define components
    text_button, a_list = "Set password", []
    if pathname == PATH_LOGIN:
        text_button, a_list = "Log in", [
            html.A("Sign up", href=PATH_SIGNUP),
            html.A("Forgot password?", href=PATH_FORGOTPWD),
        ]
    elif pathname == PATH_SIGNUP:
        text_button, a_list = "Verify the email", [
            html.A("Log in", href=PATH_LOGIN),
            html.A("Forgot password?", href=PATH_FORGOTPWD),
        ]
    elif pathname == PATH_FORGOTPWD:
        text_button, a_list = "Verify the email", [
            html.A("Log in", href=PATH_LOGIN),
            html.A("Sign up", href=PATH_SIGNUP),
        ]

    # define components
    src_image = dash.get_asset_url(kwargs.get("src_image"))
    col_left = fac.AntdCol(html.Div(children=[
        fac.AntdImage(src=src_image, preview=False),
    ], className="w-100"), span=20, md=8, className="d-flex align-items-center")

    # define components
    kwargs_button = dict(type="primary", size="large", block=True, autoSpin=True)
    col_right = fac.AntdCol(html.Div(children=[
        html.Div(kwargs["text_title"], className="text-center fs-2"),
        html.Div(kwargs["text_subtitle"], className="text-center text-muted"),

        fac.AntdForm(kwargs["form_items"], id=f"id-{tag}-form", className="mt-4"),
        fac.AntdButton(text_button, id=f"id-{tag}-button", **kwargs_button),

        fac.AntdRow(a_list, align="middle", justify="space-between", className="mt-1"),
    ], className="w-100"), span=20, md=6, className="d-flex align-items-center")

    # return result
    return fac.AntdRow(children=[
        col_left, col_right,
        # define components
        fuc.FefferyExecuteJs(id=f"id-{tag}-executejs"),
        dcc.Store(id=f"id-{tag}-data", data=kwargs["data"]),
    ], align="middle", justify="center", gutter=60, className="vh-100")
