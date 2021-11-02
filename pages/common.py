# _*_ coding: utf-8 _*_

"""
common variable / layout of page
"""

import dash_bootstrap_components as dbc
from dash import html

from layouts import adaptive

from .paths import *

# define args of components
ARGS_BUTTON_SUBMIT = {"size": "lg", "class_name": "w-100"}

# define class of components
CLASS_LABEL_ERROR = "text-danger text-center w-100 mx-auto my-0"

# define class of components
CLASS_DIV_CATALOG = "side-class bg-light border-bottom px-3 py-2"
CLASS_DIV_CONTENT = "d-flex flex-column flex-md-row h-100 overflow-scroll gx-0"

# define components
COMP_A_LOGIN = html.A("Sign in", href=PATH_LOGIN)
COMP_A_REGISTER = html.A("Sign up", href=PATH_EMAIL_REGISTER)
COMP_A_RESETPWD = html.A("Forget password?", href=PATH_EMAIL_RESETPWD)

# define components
COMP_I_LIST = html.A(html.I(className="bi bi-list fs-1"))


def layout_form(text_hd, text_sub, form, button, others):
    """
    form layout, with button and others
    """
    class_tmp = "" if form else "mt-2"
    class_sub = f"text-center text-muted {class_tmp}"
    return [
        html.Div(text_hd, className="text-center fs-1"),
        html.Div(text_sub, className=class_sub),
        html.Div(form, className="mt-4"),
        html.Div(button, className="mt-4"),
        dbc.Row(children=[
            dbc.Col(others[0], width="auto"),
            dbc.Col(others[1], width="auto"),
        ], justify="between", class_name="gx-0 mt-1"),
    ]


def layout_salert(text_hd, text_sub, text_button, return_href):
    """
    simple alert layout, only text and no image
    """
    button = dbc.Button(text_button, href=return_href, **ARGS_BUTTON_SUBMIT)
    return adaptive.layout_two(layout_form(text_hd, text_sub, None, button, [None, None]))
