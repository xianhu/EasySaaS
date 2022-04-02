# _*_ coding: utf-8 _*_

"""
intros component
"""

import dash_bootstrap_components as dbc
from dash import html

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


def layout(class_name=None):
    """
    layout of component
    """
    # define components
    intros_list = [html.Div(children=[
        html.I(className=f"{item[0]} fs-4 text-primary"),
        html.Div(item[1], className="fs-5 my-1"),
        html.P(item[2], className="text-muted"),
    ]) for item in INTROS_LIST]

    # return result
    return dbc.Row(children=[
        dbc.Col(intros_list[0], width=10, md=3, class_name=None),
        dbc.Col(intros_list[1], width=10, md=3, class_name="mt-4 mt-md-0"),
        dbc.Col(intros_list[2], width=10, md=3, class_name="mt-4 mt-md-0"),
    ], align="center", justify="around", class_name=class_name)
