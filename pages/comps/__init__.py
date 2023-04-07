# _*_ coding: utf-8 _*_

"""
components module
"""

from dash import html

from config import CONFIG_APP_NAME
from utility.paths import PATH_ROOT


def get_component_logo(style_logo=None):
    """
    layout of component
    """
    # define style
    style_logo = {
        "color": "#000000",
        "font-size": "40px",
        "font-weight": "900",
        "font-family": "Raleway",
        "text-decoration": "none",
    } if not style_logo else style_logo

    # return result
    return html.A(CONFIG_APP_NAME, href=PATH_ROOT, style=style_logo)
