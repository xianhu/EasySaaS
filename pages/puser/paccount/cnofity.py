# _*_ coding: utf-8 _*_

"""
Notifications
"""

import dash_bootstrap_components as dbc
from dash import html

TAG = "user-notify"
NOTIFICATIONS = [
    "The Standard License grants you a non-exclusive right to make use of Theme you have purchased.",
    "You are licensed to use the Item to create one End Product for yourself or for one client (a “single application”), and the End Product can be distributed for Free.",
    "This license can be terminated if you breach it and you lose the right to distribute the End Product until the Theme has been fully removed from the End Product.",
    "The author of the Theme retains ownership of the Theme, but grants you the license on these terms. This license is between the author of the Theme and you. ",
    "Be Colossal LLC (Bootstrap Themes) are not a party to this license or the one granting you the license.",
]


def layout(pathname, search):
    """
    layout of card
    """
    return dbc.Card(children=[
        dbc.Row(children=[
            dbc.Col("Notifications:", width="auto"),
            dbc.Col(dbc.Switch(id=f"id-{TAG}-switch", value=True), width="auto"),
        ], align="center", justify="between", class_name="gx-0 border-bottom p-4"),
        html.Div(html.Ul([html.Li(notify, className="my-2") for notify in NOTIFICATIONS]), className="p-4"),
    ], class_name="mb-4")