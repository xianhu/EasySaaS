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
    class_text = f"fs-5 text-white align-middle ms-1 {class_text}"

    # return result
    return dbc.NavbarBrand(children=[
        html.Img(src=src_logo, style={"width": "1.5rem"}),
        html.Span(config_app_name, className=class_text),
    ], href=href, class_name=class_name)
