# _*_ coding: utf-8 _*_

"""
pricing of page
"""

import dash_bootstrap_components as dbc
from dash import html

PLAN_LIST = [{
    "name": "Basic",
    "price": "$10/M",
    "descs": [
        "project count: 1",
        "member count: 3 / project",
        "analysis count: 100 / day",
    ]
}, {
    "name": "Standard",
    "price": "$30/M",
    "descs": [
        "project count: 5",
        "member count: 20 / project",
        "analysis count: 1000 / day",
    ]
}, {
    "name": "Enhanced",
    "price": "$100/M",
    "descs": [
        "project count: no limit",
        "member count: 100 / project",
        "analysis count: 5000 / day",
    ]
}]


def layout(pathname, search):
    """
    layout of components
    """
    col_list = []
    for plan in PLAN_LIST:
        col_list.append(dbc.Col(children=[
            html.Div(plan["name"], className="fs-5 fw-bold"),
            html.Div(plan["price"], className="fs-6 fw-bold"),
            html.Div([html.Li(desc) for desc in plan["descs"]], className=None),
            dbc.Button("Buy it", class_name="w-50 mt-4"),
        ], width=12, md=3, class_name="border rounded text-center p-4 mt-2 mt-md-0"))
    return html.Div(dbc.Row(col_list, justify="around", class_name="m-4"))
