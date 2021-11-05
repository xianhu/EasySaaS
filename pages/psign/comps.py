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
COMP_A_REGISTER = html.A("Sign up", href=PATH_REGISTERE)
COMP_A_RESETPWD = html.A("Forget password?", href=PATH_RESETPWDE)

