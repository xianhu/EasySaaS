# _*_ coding: utf-8 _*_

"""
template of sign page
"""

import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html

from ..comps import get_component_logo
from ..paths import PATH_FORGOTPWD, PATH_LOGIN, PATH_SIGNUP

# define components
a_log_in = html.A("Log in", href=PATH_LOGIN)
a_sign_up = html.A("Sign up", href=PATH_SIGNUP)
a_forgot_pwd = html.A("Forgot password?", href=PATH_FORGOTPWD)


def layout(pathname, search, tag, **kwargs):
    """
    layout of template
    """
    # define components
    text_button, a_list = "Set password", []
    if pathname == PATH_LOGIN:
        text_button, a_list = "Log in", [a_sign_up, a_forgot_pwd]
    elif pathname == PATH_SIGNUP:
        text_button, a_list = "Verify the email", [a_log_in, a_forgot_pwd]
    elif pathname == PATH_FORGOTPWD:
        text_button, a_list = "Verify the email", [a_log_in, a_sign_up]

    # define components
    kwargs_button = dict(type="primary", size="large", block=True, autoSpin=True)
    content = html.Div(children=[
        html.Div(kwargs["text_title"], className="text-center fs-3"),
        html.Div(kwargs["text_subtitle"], className="text-center text-muted"),

        fac.AntdForm(kwargs["form_items"], id=f"id-{tag}-form", className="mt-4"),
        fac.AntdButton(text_button, id=f"id-{tag}-button", **kwargs_button),

        fac.AntdRow(a_list, align="middle", justify="space-between", className="mt-2"),
    ], className="bg-white shadow rounded p-4")

    # return result
    return html.Div(children=[
        html.Div(get_component_logo(size=40), className="text-center mt-5 mb-4"),
        fac.AntdRow(fac.AntdCol(content, span=20, md=6), justify="center"),
        # define components
        fuc.FefferyExecuteJs(id=f"id-{tag}-executejs"),
        dcc.Store(id=f"id-{tag}-data", data=kwargs["data"]),
    ], className="vh-100 overflow-auto")
