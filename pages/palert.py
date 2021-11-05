# _*_ coding: utf-8 _*_

"""
alert page
"""

import flask

import dash_bootstrap_components as dbc
from dash import html


def _simple_alert(text_hd, text_sub, text_button, return_href):
    """
    simple alert layout, only text and no image
    """
    return dbc.Row(dbc.Col(children=[
        html.Div(text_hd, className="text-center fs-1"),
        html.Div(text_sub, className="text-center text-muted mt-2"),
        dbc.Button(text_button, href=return_href, size="lg", class_name="w-100 mt-4"),
    ], width=10, md=3), align="center", justify="center", class_name="vh-100 w-100")


def layout_404(pathname, search, return_href):
    """
    layout of page
    """
    text_hd = "Page not found"
    text_sub = "This page is not found, click button to safe page."
    return _simple_alert(text_hd, text_sub, "Back to safety", return_href)


def layout_expire(pathname, search, return_href):
    """
    layout of page
    """
    text_hd = "Link expired"
    text_sub = "The link has already expired, click button to safe page."
    return _simple_alert(text_hd, text_sub, "Back to safety", return_href)


def layout_email(pathname, search, return_href):
    """
    layout of page
    """
    email = flask.session.get("email", "")
    text_hd = "Sending success"
    text_sub = f"An email has sent to [{email}], go mailbox to verify it."
    return _simple_alert(text_hd, text_sub, "Back to home", return_href)


def layout_password(pathname, search, return_href):
    """
    layout of page
    """
    text_hd = "Setting success"
    text_sub = "The password was set successfully."
    return _simple_alert(text_hd, text_sub, "Go to login", return_href)
