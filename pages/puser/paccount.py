# _*_ coding: utf-8 _*_

"""
page of user account
"""

import dash_bootstrap_components as dbc
import flask_login
from dash import html

TAG = "user-account"


def layout(pathname, search):
    """
    layout of page
    """
    email = flask_login.current_user.email
    card1 = dbc.Card(children=[
        html.Div("Basic Information:", className="border-bottom p-4"),
        dbc.Row(children=[
            dbc.Col(dbc.FormFloating(children=[
                dbc.Input(id=f"id-{TAG}-email", type="email", value=email, disabled=True),
                dbc.Label("Email:", html_for=f"id-{TAG}-email"),
            ]), width=12, md=4, class_name=""),
            dbc.Col(dbc.FormFloating(children=[
                dbc.Input(id=f"id-{TAG}-nickname", type="text"),
                dbc.Label("NickName:", html_for=f"id-{TAG}-nickname"),
            ]), width=12, md=4, class_name="mt-2 mt-md-0"),
            dbc.Col(dbc.FormFloating(children=[
                dbc.Input(id=f"id-{TAG}-phone", type="tel"),
                dbc.Label("Phone:", html_for=f"id-{TAG}-phone"),
            ]), width=12, md=4, class_name="mt-2 mt-md-0"),
            dbc.Col(children=[
                dbc.Button("Update Information", id=f"id-{TAG}-button", class_name="w-100"),
            ], width=12, md=4, class_name="mt-4 mt-md-4"),
        ], class_name="p-4"),
    ], class_name="mb-4")

    card2 = dbc.Card(children=[
        html.Div("Change Password:", className="border-bottom p-4"),
        dbc.Row(children=[
            dbc.Col(dbc.FormFloating(children=[
                dbc.Input(id=f"id-{TAG}-pwd", type="password"),
                dbc.Label("Current Password:", html_for=f"id-{TAG}-pwd"),
            ]), width=12, md=4, class_name=""),
            dbc.Col(dbc.FormFloating(children=[
                dbc.Input(id=f"id-{TAG}-pwd1", type="password"),
                dbc.Label("New Password:", html_for=f"id-{TAG}-pwd1"),
            ]), width=12, md=4, class_name="mt-2 mt-md-0"),
            dbc.Col(dbc.FormFloating(children=[
                dbc.Input(id=f"id-{TAG}-pwd2", type="password"),
                dbc.Label("Confirm Password:", html_for=f"id-{TAG}-pwd2"),
            ]), width=12, md=4, class_name="mt-2 mt-md-0"),
            dbc.Col(children=[
                dbc.Button("Update Password", id=f"id-{TAG}-button", class_name="w-100"),
            ], width=12, md=4, class_name="mt-4 mt-md-4"),
        ], class_name="p-4 mt-4"),
    ], class_name="mb-4")

    notifications = [
        "The Standard License grants you a non-exclusive right to make use of Theme you have purchased.",
        "You are licensed to use the Item to create one End Product for yourself or for one client (a “single application”), and the End Product can be distributed for Free.",
        "This license can be terminated if you breach it and you lose the right to distribute the End Product until the Theme has been fully removed from the End Product.",
        "The author of the Theme retains ownership of the Theme, but grants you the license on these terms. This license is between the author of the Theme and you. ",
        "Be Colossal LLC (Bootstrap Themes) are not a party to this license or the one granting you the license.",
    ]

    card3 = dbc.Card(children=[
        html.Div("Notifications:", className="border-bottom p-4"),
        html.Div(html.Ul([html.Li(notify, className="mb-4") for notify in notifications]), className="p-4"),
    ], class_name="mb-4")
    return [card1, card2, card3]
