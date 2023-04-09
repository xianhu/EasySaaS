# _*_ coding: utf-8 _*_

"""
template of sign page
"""

import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html

from utility.paths import PATH_FORGOTPWD, PATH_LOGIN, PATH_SIGNUP
from ..comps import get_component_logo


def layout(pathname, search, tag, **kwargs):
    """
    layout of template
    """
    # define components
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
    else:
        text_button, a_list = "Set password", []

    # define components
    kwargs_button = dict(type="primary", size="large", block=True, autoSpin=True)
    content = html.Div(children=[
        html.Div(kwargs["text_title"], className="text-center fs-3"),
        html.Div(kwargs["text_subtitle"], className="text-center text-muted"),

        # define components
        fac.AntdForm(kwargs["form_items"], id=f"id-{tag}-form", className="mt-4"),

        # define components
        fac.AntdButton(text_button, id=f"id-{tag}-button", **kwargs_button, className=None),
        fac.AntdRow(a_list, align="middle", justify="space-between", className="mt-2"),
    ], className="bg-white shadow rounded p-4")

    # return result
    return html.Div(children=[
        html.Div(get_component_logo(size=40), className="text-center pt-5 pb-4"),
        fac.AntdRow(fac.AntdCol(content, span=20, md=6), justify="center", className=None),
        # define components
        fuc.FefferyExecuteJs(id=f"id-{tag}-executejs"),
        dcc.Store(id=f"id-{tag}-data", data=kwargs["data"]),
    ], className="vh-100 overflow-auto")
