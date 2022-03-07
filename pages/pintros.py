# _*_ coding: utf-8 _*_

"""
intros page
"""

import dash
import dash_bootstrap_components as dbc
from dash import html

from .components import cfooter, cnavbar

TAG = "intros"

HEADER = "Welcome to EasySaaS demo"
HEADERSUB = """
This project will be attempted to make a great starting point for your next big business as easy and efficent as possible. 
This project will create an easy way to build a SaaS application using Python and Dash.
""".strip()

INTROS_LIST = [[
    "bi bi-code-slash",
    "Built for developers",
    "EasySaaS is built to make your life easier. Variables, build tooling, documentation, and reusable components.",
], [
    "bi bi-view-list",
    "Designed to be modern",
    "Designed with the latest design trends in mind. EasySaaS feels modern, minimal, and beautiful.",
], [
    "bi bi-list-stars",
    "Documentation for everything",
    "We've written extensive documentation for components and tools, so you never have to reverse engineer anything.",
]]

PLAN_LIST = [{
    "name": "Basic", "price": "$10/M", "descs": [
        "project count: 1",
        "member count: 3 / project",
        "analysis count: 100 / day",
    ]}, {
    "name": "Standard", "price": "$30/M", "descs": [
        "project count: 5",
        "member count: 20 / project",
        "analysis count: 1000 / day",
    ]}, {
    "name": "Enhanced", "price": "$100/M", "descs": [
        "project count: no limit",
        "member count: 100 / project",
        "analysis count: 5000 / day",
    ]}
]

CONTACT_HEADER = "Let us hear from you directly!"
CONTACT_HEADERSUB = "We always want to hear from you! Let us know how we can best help you and we'll do our very best."


def layout(pathname, search):
    """
    layout of page
    """
    # define class
    class_col = "mt-4 mt-md-0"
    class_row = "w-100 mx-auto"

    # define components
    image = html.Img(src=dash.get_asset_url("illustrations/intros.svg"), className="img-fluid")
    intros = [
        html.Div(HEADER, className="fs-1 text-center mb-2"),
        html.P(HEADERSUB, className="fs-5 text-center text-muted lead"),
    ]
    content1 = dbc.Row(children=[
        dbc.Col(image, width=10, md={"size": 5, "order": 2}, class_name=None),
        dbc.Col(intros, width=10, md={"size": 5, "order": 1}, class_name=class_col),
    ], align="center", justify="around", class_name=class_row)

    # define components
    intros_list = [[
        html.I(className=f"{item[0]} fs-4 text-primary"),
        html.Div(item[1], className="fs-5 my-1"),
        html.P(item[2], className="text-muted"),
    ] for item in INTROS_LIST]
    content2 = dbc.Row(children=[
        dbc.Col(intros_list[0], width=10, md=3, class_name=None),
        dbc.Col(intros_list[1], width=10, md=3, class_name=class_col),
        dbc.Col(intros_list[2], width=10, md=3, class_name=class_col),
    ], align="center", justify="around", class_name=f"{class_row} mt-5")

    # define components
    plan_list = [dbc.Card(children=[
        html.Div(plan["name"], className="fs-2"),
        html.Div(plan["price"], className="text-primary"),
        html.Div([html.Li(desc) for desc in plan["descs"]], className="lh-lg"),
        dbc.Button("Buy it now", id=f"id-{TAG}-{plan['name']}", class_name="w-75 mt-4"),
    ], body=True, class_name="text-center p-3") for plan in PLAN_LIST]
    content3 = dbc.Row(children=[
        dbc.Col(plan_list[0], width=10, md=3, class_name=None),
        dbc.Col(plan_list[1], width=10, md=3, class_name=class_col),
        dbc.Col(plan_list[2], width=10, md=3, class_name=class_col),
    ], align="center", justify="around", class_name=f"{class_row} mt-5")

    # define components
    content4 = dbc.Row(children=[
        dbc.Col(children=[
            html.Div(CONTACT_HEADER, className="fs-2 text-center"),
            html.P(CONTACT_HEADERSUB, className="fs-6 text-center text-muted"),
        ], width=12, md=6),
    ], align="center", justify="around", class_name=f"{class_row} mt-5")

    # define components
    content5 = dbc.Row(children=[
        dbc.Col(dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-email", type="email"),
            dbc.Label("Email:", html_for=f"id-{TAG}-email"),
        ]), width=12, md=4, class_name=None),
        dbc.Col(dbc.FormFloating(children=[
            dbc.Input(id=f"id-{TAG}-name", type="text"),
            dbc.Label("FullName:", html_for=f"id-{TAG}-name"),
        ]), width=12, md=4, class_name=class_col),
        dbc.Col(dbc.Textarea(
            id=f"id-{TAG}-content", rows=4,
            placeholder="Tell us what we can help you with!",
        ), width=12, md=8, class_name=f"{class_col} mt-md-4"),
        dbc.Col(children=[
            dbc.Button("Send message", id=f"id-{TAG}-button"),
        ], width=12, md=8, class_name=f"{class_col} mt-md-4 text-center"),
    ], align="center", justify="center", class_name=f"{class_row} mt-2")

    # define components
    contentt = dbc.Row(children=[
        dbc.Col(children=[
            dbc.Checkbox(label="Checkbox", value=True),
            dbc.Switch(label="Toggle switch", value=True),
            dbc.RadioButton(label="Radio button", value=True),
        ], width=10, md=3, class_name=None),
        dbc.Col(dbc.RadioItems(options=[
            {"label": "Option 1", "value": 1},
            {"label": "Option 2", "value": 2},
            {"label": "Disabled Option", "value": 3, "disabled": True},
        ], value=1), width=10, md=3, class_name=class_col),
        dbc.Col(dbc.Checklist(options=[
            {"label": "Option 1", "value": 1},
            {"label": "Option 2", "value": 2},
            {"label": "Disabled Option", "value": 3, "disabled": True},
        ], value=[1]), width=10, md=3, class_name=class_col),
        dbc.Col(dbc.Select(options=[
            {"label": "Option 1", "value": "1"},
            {"label": "Option 2", "value": "2"},
            {"label": "Disabled Option", "value": "3", "disabled": True},
        ], value=1), width=10, md=3, class_name=class_col),
    ], align="center", justify="around", className=f"{class_row} mt-5")

    # define components
    navbar = cnavbar.layout(pathname, search, fluid=None)
    footer = cfooter.layout(pathname, search, fluid=None)
    content = [content1, content2, content3, content4, content5, contentt]

    # return result
    return html.Div([navbar, dbc.Container(content, class_name="py-5"), footer], className=None)
