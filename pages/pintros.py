# _*_ coding: utf-8 _*_

"""
intros page
"""

import dash_bootstrap_components as dbc
from dash import html

from .comps import cfooter, cnavbar
from .paths import *

HEADER = "Welcome to EasySaaS demo"
HEADERSUB = """
This project will be attempt to make a great starting point 
for your next big business as easy and efficent as possible. 
This project will create an easy way to build a SaaS application using Python and Dash.
"""

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
    ]
}, {
    "name": "Standard", "price": "$30/M", "descs": [
        "project count: 5",
        "member count: 20 / project",
        "analysis count: 1000 / day",
    ]
}, {
    "name": "Enhanced", "price": "$100/M", "descs": [
        "project count: no limit",
        "member count: 100 / project",
        "analysis count: 5000 / day",
    ]
}]


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    image_src = "assets/illustrations/intros.svg"
    image = html.Img(src=image_src, className="img-fluid")
    intros = [
        html.Div(HEADER, className="fs-1 mb-2"),
        html.P(HEADERSUB, className="fs-5 text-muted lead"),
    ]

    # define components
    intros_list = []
    for item in INTROS_LIST:
        intros_list.append([
            html.I(className=f"{item[0]} fs-4 text-primary"),
            html.Div(item[1], className="fs-5 my-1"),
            html.P(item[2], className="text-muted"),
        ])

    # define components
    plan_list = []
    for plan in PLAN_LIST:
        desc_list = [html.Li(desc) for desc in plan["descs"]]
        plan_list.append([
            html.Div(plan["name"], className="fs-2"),
            html.Div(plan["price"], className="text-primary"),
            html.Div(desc_list, className="lh-lg"),
            dbc.Button("Buy it now", class_name="w-75 mt-4"),
        ])

    # define
    fluid = None
    class_col = "mt-4 mt-md-0"
    class_row = "w-100 mx-auto my-5"
    class_col_price = f"{class_col} border rounded-3 py-4"

    # define components
    content = dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(image, width=10, md={"size": 5, "order": 2}, class_name=None),
            dbc.Col(intros, width=10, md={"size": 5, "order": 1}, class_name=class_col),
        ], align="center", justify="around", class_name=f"{class_row} text-center"),
        dbc.Row(children=[
            dbc.Col(intros_list[0], width=10, md=3, class_name=class_col),
            dbc.Col(intros_list[1], width=10, md=3, class_name=class_col),
            dbc.Col(intros_list[2], width=10, md=3, class_name=class_col),
        ], align="start", justify="around", class_name=f"{class_row} py-4"),
        dbc.Row(children=[
            dbc.Col(plan_list[0], width=10, md=3, class_name=class_col_price),
            dbc.Col(plan_list[1], width=10, md=3, class_name=class_col_price),
            dbc.Col(plan_list[2], width=10, md=3, class_name=class_col_price),
        ], align="center", justify="around", class_name=f"{class_row} text-center"),
    ], fluid=fluid)

    # define components
    navbar = cnavbar.layout(pathname, search, fluid=fluid)
    footer = cfooter.layout(pathname, search, fluid=fluid)

    # return result
    return [navbar, content, footer]
