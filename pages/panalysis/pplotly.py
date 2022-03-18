# _*_ coding: utf-8 _*_

"""
plotly page
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

from ..components3 import cplotly


def layout(pathname, search, _type):
    """
    layout of page
    """
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

    # return result
    return dbc.Card(children=[
        dbc.CardHeader(f"Plotly Page: {_type}", class_name="px-4 py-3"),
        html.Div(children, className="p-0"),
    ], class_name=None, style={"minHeight": "600px"})
