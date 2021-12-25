# _*_ coding: utf-8 _*_

"""
account page
"""

from dash import html

from . import cbasic, cnofity, cpwd


def layout(pathname, search):
    """
    layout of page
    """
    return html.Div(children=[
        cbasic.layout(pathname, search),
        cpwd.layout(pathname, search),
        cnofity.layout(pathname, search),
    ])
