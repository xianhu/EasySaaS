# _*_ coding: utf-8 _*_

"""
"""

import dash_bootstrap_components as dbc
from dash import html

from ..paths import *

# define args of components
ARGS_BUTTON_SUBMIT = {"size": "lg", "class_name": "w-100"}

# define class of components
CLASS_LABEL_ERROR = "text-danger text-center w-100 mx-auto my-0"

# define components
COMP_A_LOGIN = html.A("Sign in", href=PATH_LOGIN)
COMP_A_REGISTER = html.A("Sign up", href=PATH_REGISTER_E)
COMP_A_RESETPWD = html.A("Forget password?", href=PATH_RESETPWD_E)

# define components
COMP_I_LIST = html.A(html.I(className="bi bi-list fs-1"))


def layout_form(text_hd, text_sub, form, button, others):
    """
    form layout, with button and others
    """
    return [
        html.Div(text_hd, className="text-center fs-1"),
        html.Div(text_sub, className="text-center text-muted"),
        html.Div(form, className="mt-4"),
        html.Div(button, className="mt-4"),
        dbc.Row(children=[
            dbc.Col(others[0], width="auto"),
            dbc.Col(others[1], width="auto"),
        ], justify="between", class_name="w-100 mt-1"),
    ]
