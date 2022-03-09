# _*_ coding: utf-8 _*_

"""
layout of plans
"""

from dash import html
import dash_bootstrap_components as dbc

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


def layout(pathname, search):
    """
    layout of plans
    """
    # define components
    plan_list = [dbc.Card(children=[
        html.Div(plan["name"], className="fs-2"),
        html.Div(plan["price"], className="text-primary"),
        html.Div([html.Li(desc) for desc in plan["descs"]], className="lh-lg"),
        dbc.Button("Buy it now", class_name="w-75 mt-4"),
    ], body=True, class_name="text-center p-3") for plan in PLAN_LIST]

    # return result
    return dbc.Row(children=[
        dbc.Col(plan_list[0], width=10, md=3, class_name=None),
        dbc.Col(plan_list[1], width=10, md=3, class_name="mt-4 mt-md-0"),
        dbc.Col(plan_list[2], width=10, md=3, class_name="mt-4 mt-md-0"),
    ], align="center", justify="around", class_name="mt-5")
