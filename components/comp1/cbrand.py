# _*_ coding: utf-8 _*_

"""
brand component
"""

import dash
import dash_bootstrap_components as dbc
from dash import html

from config import config_app_name


def layout(pathname, search, class_name=None):
    """
    layout of component
    """
    # define components
    img = html.Img(src=dash.get_asset_url("favicon.svg"), style={"width": "1.2rem"})
    span = html.Span(config_app_name, className="fs-5 align-middle ms-1")

    # return result
    return dbc.NavbarBrand([img, span], href="/", class_name=class_name)
