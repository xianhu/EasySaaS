# _*_ coding: utf-8 _*_

"""
catalog of analysis
"""

import dash_bootstrap_components as dbc
from dash import html


def layout_catalog():
    """
    layout of catalog
    """
    class_li = "cursor-pt text-hover-primary mt-2"
    return html.Div(children=[
        dbc.Button("Add File", className="w-100"),
        html.Div("GETTING STARTED", className="h6 mt-4"),
        html.Ul(children=[
            html.Li("module 11", className=class_li),
            html.Li("module 12", className=class_li),
            html.Li("module 13", className=class_li),
            html.Li("module 14", className=class_li),
            html.Li("module 15", className=class_li),
        ], className="", style={"padding-inline-start": "20px"}),
        html.Div("GETTING STARTED", className="h6 mt-4"),
        html.Ul(children=[
            html.Li("module 11", className=class_li),
            html.Li("module 12", className=class_li),
            html.Li("module 13", className=class_li),
            html.Li("module 14", className=class_li),
            html.Li("module 15", className=class_li),
        ], className=""),
        html.Div("GETTING STARTED", className="h6 mt-4"),
        html.Ul(children=[
            html.Li("module 11", className=class_li),
            html.Li("module 12", className=class_li),
            html.Li("module 13", className=class_li),
            html.Li("module 14", className=class_li),
            html.Li("module 15", className=class_li),
        ], className=""),
        html.Div("GETTING STARTED", className="h6 mt-4"),
        html.Ul(children=[
            html.Li("module 11", className=class_li),
            html.Li("module 12", className=class_li),
            html.Li("module 13", className=class_li),
            html.Li("module 14", className=class_li),
            html.Li("module 15", className=class_li),
        ], className=""),
    ])
