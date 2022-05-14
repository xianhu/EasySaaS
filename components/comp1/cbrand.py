# _*_ coding: utf-8 _*_

"""
brand component
"""

import dash
import dash_bootstrap_components as dbc
from dash import html

from config import config_app_name
from utility.paths import PATH_ROOT


def layout(href=PATH_ROOT, class_text=None, class_name=None):
    """
    layout of component
    """
    # define variables
    src_logo = dash.get_asset_url("favicon.svg")
    class_text = class_text or "fs-5 align-middle ms-1"

    # return result
    return dbc.NavbarBrand(children=[
        html.Img(src=src_logo, style={"width": "1.2rem"}),
        html.Span(config_app_name, className=class_text),
    ], href=href, class_name=class_name)
