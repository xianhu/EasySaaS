# _*_ coding: utf-8 _*_

"""
contact component
"""

from dash import html
import dash_bootstrap_components as dbc

TAG = "intros-contact"
HEADER = "Let us hear from you directly!"
HEADERSUB = "We always want to hear from you! Let us know how we can best help you and we'll do our very best."


def layout(pathname, search):
    """
    layout of component
    """
    # define components
    c_email = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-email", type="email"),
        dbc.Label("Email:", html_for=f"id-{TAG}-email"),
    ])
    c_name = dbc.FormFloating(children=[
        dbc.Input(id=f"id-{TAG}-name", type="text"),
        dbc.Label("FullName:", html_for=f"id-{TAG}-name"),
    ])
    c_text = dbc.Textarea(
        id=f"id-{TAG}-text", rows=4,
        placeholder="Tell us what we can help you with!",
    )
    c_button = dbc.Button("Send message", id=f"id-{TAG}-button")

    # return result
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col(children=[
                html.Div(HEADER, className="fs-2 text-center"),
                html.P(HEADERSUB, className="fs-6 text-center text-muted"),
            ], width=12, md=6),
        ], align="center", justify="center", class_name=None),
        dbc.Row(children=[
            dbc.Col(c_email, width=12, md=4, class_name=None),
            dbc.Col(c_name, width=12, md=4, class_name="mt-4 mt-md-0"),
            dbc.Col(c_text, width=12, md=8, class_name="mt-4 mt-md-4"),
            dbc.Col(c_button, width=12, md=8, class_name="mt-4 mt-md-4 text-center"),
        ], align="center", justify="center", class_name="mt-2")
    ], className="mt-5")
