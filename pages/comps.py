# _*_ coding: utf-8 _*_

"""
components of page
"""

from dash import html
import dash_bootstrap_components as dbc

from layouts import adaptive

from .consts import *

# define args of components
ARGS_BUTTON_SUBMIT = {"size": "lg", "class_name": "w-100"}

# define class of components
CLAS_LABEL_ERROR = "text-danger text-center w-100 mx-auto my-0"

# define components
COMP_A_LOGIN = html.A("Sign in", href=PATH_LOGIN)
COMP_A_REGISTER = html.A("Sign up", href=PATH_REGISTER_EMAIL)
COMP_A_RESET = html.A("Forget password?", href=PATH_RESET_EMAIL)


def layout_form(text_hd, text_sub, form, button, others):
    """
    form layout, with button and others
    """
    class_tmp = "" if form else "mt-2"
    class_sub = f"text-center text-muted {class_tmp}"
    return [
        dbc.Container(text_hd, class_name="text-center fs-1"),
        dbc.Container(text_sub, class_name=class_sub),
        dbc.Container(form, class_name="mt-4"),
        dbc.Container(button, class_name="mt-4"),
        dbc.Row(children=[
            dbc.Col(others[0], width="auto"),
            dbc.Col(others[1], width="auto"),
        ], justify="between", class_name="gx-0 mt-1"),
    ]


def layout_salert(text_hd, text_sub, text_button, href="/"):
    """
    simple alert layout, only text and no image
    """
    button = dbc.Button(text_button, href=href, **ARGS_BUTTON_SUBMIT)
    form = layout_form(text_hd, text_sub, None, button, [None, None])
    return adaptive.layout_two(item_left=form, width_left=(10, 3, 3))
