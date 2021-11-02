# _*_ coding: utf-8 _*_

"""
layout of pricing
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search):
    return dbc.Row(children=[
        dbc.Col(children=[
            html.Div("Free", className="fs-5 fw-bold"),
            html.Div("$0", className="fs-6 fw-bold"),
            html.Div(children=[
                html.Li("project count: 1"),
                html.Li("member count: 3/project"),
                html.Li("analysis count: 100/day"),
            ], className=""),
            dbc.Button("Buy it", class_name="w-50 mt-2"),
        ], width=10, md=3, class_name="border py-4 bg-light text-center"),
        dbc.Col(children=[
            html.Div("Standard", className="fs-5 fw-bold"),
            html.Div("$10", className="fs-6 fw-bold"),
            html.Div(children=[
                html.Li("project count: 3"),
                html.Li("member count: 10/project"),
                html.Li("analysis count: 200/day"),
            ], className=""),
            dbc.Button("Buy it", class_name="w-50 mt-2"),
        ], width=10, md=3, class_name="border py-4 bg-light mt-4 mt-md-0 text-center"),
        dbc.Col(children=[
            html.Div("Professional", className="fs-5 fw-bold"),
            html.Div("$30", className="fs-6 fw-bold"),
            html.Div(children=[
                html.Li("project count: 10"),
                html.Li("member count: 50/project"),
                html.Li("analysis count: 1000/day"),
            ], className=""),
            dbc.Button("Buy it", class_name="w-50 mt-2"),
        ], width=10, md=3, class_name="border py-4 bg-light mt-4 mt-md-0 text-center"),
    ], justify="around", class_name="gx-0 my-4")
