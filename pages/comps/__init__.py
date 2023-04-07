# _*_ coding: utf-8 _*_

"""
components module
"""

from dash import html

from config import CONFIG_APP_NAME
from utility.paths import PATH_ROOT


def get_component_logo():
    """
    layout of component
    """
    # define style
    style_logo = {
        "font-size": "40px",
        "font-weight": "900",
        "font-family": "Raleway",
    }
    class_logo = "text-dark text-decoration-none"

    # return result
    return html.A(CONFIG_APP_NAME, href=PATH_ROOT, className=class_logo, style=style_logo)
