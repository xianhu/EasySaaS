# _*_ coding: utf-8 _*_

"""
plotly page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, dcc

from app import app
from components import cplotly

TAG = "test"


def layout(pathname, search, _type):
    """
    layout of page
    """
    # children = []
    # if _type == "scatter":
    #     children = [
    #         dcc.Graph(figure=cplotly.fig_scatter_1),
    #         dcc.Graph(figure=cplotly.fig_scatter_2),
    #         dcc.Graph(figure=cplotly.fig_scatter_3),
    #         dcc.Graph(figure=cplotly.fig_scatter_4),
    #     ]
    # elif _type == "line":
    #     children = [
    #         dcc.Graph(figure=cplotly.fig_line_1),
    #         dcc.Graph(figure=cplotly.fig_line_2),
    #         dcc.Graph(figure=cplotly.fig_line_3),
    #     ]
    # elif _type == "bar":
    #     children = [
    #         dcc.Graph(figure=cplotly.fig_bar_1),
    #         dcc.Graph(figure=cplotly.fig_bar_2),
    #         dcc.Graph(figure=cplotly.fig_bar_3),
    #         dcc.Graph(figure=cplotly.fig_bar_4),
    #         dcc.Graph(figure=cplotly.fig_bar_5),
    #     ]
    # elif _type == "pie":
    #     children = [
    #         dcc.Graph(figure=cplotly.fig_pie_1),
    #         dcc.Graph(figure=cplotly.fig_pie_2),
    #         dcc.Graph(figure=cplotly.fig_pie_3),
    #     ]

    # return result
    return dbc.Card(children=[
        dbc.CardHeader(f"Plotly Page:", class_name="px-4 py-3"),
        dbc.Spinner(children=None, id=f"id-{TAG}-content"),
        dcc.Store(id=f"id-{TAG}-store", data=_type),
    ], class_name=None, style={"minHeight": "600px"})


import time


@app.callback(
    Output(f"id-{TAG}-content", "children"),
    Input(f"id-{TAG}-store", "data"),
    prevent_initial_call=False,
)
def _test(_type):
    time.sleep(5)

    children = []
    if _type == "scatter":
        children = [
            dcc.Graph(figure=cplotly.fig_scatter_1),
            dcc.Graph(figure=cplotly.fig_scatter_2),
            dcc.Graph(figure=cplotly.fig_scatter_3),
            dcc.Graph(figure=cplotly.fig_scatter_4),
        ]
    elif _type == "line":
        children = [
            dcc.Graph(figure=cplotly.fig_line_1),
            dcc.Graph(figure=cplotly.fig_line_2),
            dcc.Graph(figure=cplotly.fig_line_3),
        ]
    elif _type == "bar":
        children = [
            dcc.Graph(figure=cplotly.fig_bar_1),
            dcc.Graph(figure=cplotly.fig_bar_2),
            dcc.Graph(figure=cplotly.fig_bar_3),
            dcc.Graph(figure=cplotly.fig_bar_4),
            dcc.Graph(figure=cplotly.fig_bar_5),
        ]
    elif _type == "pie":
        children = [
            dcc.Graph(figure=cplotly.fig_pie_1),
            dcc.Graph(figure=cplotly.fig_pie_2),
            dcc.Graph(figure=cplotly.fig_pie_3),
        ]
    return children
