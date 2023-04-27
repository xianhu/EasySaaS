# _*_ coding: utf-8 _*_

"""
components module
"""

from dash import html

from core.settings import settings
from ..paths import PATH_ROOT


def get_component_logo(size):
    """
    layout of component
    """
    return html.A(style={
        "color": "#000000",
        "font-weight": "900",
        "font-size": f"{size}px",
        "font-family": "Raleway-Bold",
        "text-decoration": "none",
    }, children=settings.APP_NAME, href=PATH_ROOT)
