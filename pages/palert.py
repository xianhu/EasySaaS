# _*_ coding: utf-8 _*_

"""
alert page
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search, text_hd, text_sub, text_button, return_href):
    """
    layout of page, only text and button, no image
    """
    return dbc.Row(dbc.Col(children=[
        html.Div(text_hd, className="text-center fs-1"),
        html.Div(text_sub, className="text-center text-muted mt-2"),
        dbc.Button(text_button, href=return_href, size="lg", class_name="w-100 mt-4"),
    ], width=10, md=3), align="center", justify="center", class_name="vh-100 w-100 mx-auto")


def layout_404(pathname, search, return_href="/"):
    """
    layout of page
    """
    text_hd = "Page not found"
    text_sub = "This page is not found, click button to safe page."
    return layout(pathname, search, text_hd, text_sub, "Back to safety", return_href)


def layout_500(pathname, search, return_href="/"):
    """
    layout of page
    """
    text_hd = "An error occurred"
    text_sub = "A server error has occurred, click button to safe page."
    return layout(pathname, search, text_hd, text_sub, "Back to safety", return_href)
