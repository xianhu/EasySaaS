# _*_ coding: utf-8 _*_

"""
table page
"""

import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html

from components import ctable

TAG = "analysis-table"
DATA = px.data.iris()


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    args = {"size": "sm", "color": "primary", "outline": True}
    button = dbc.Button("Download File", id=f"id-{TAG}-button", **args)

    # define components
    row_header = dbc.Row(children=[
        dbc.Col("Table Page", width="auto", class_name=None),
        dbc.Col(button, width="auto", class_name=None),
    ], align="center", justify="between", class_name=None)

    # define components
    table_0 = ctable.layout(
        pathname, search, f"id-{TAG}-table1", DATA.to_dict("records")[:10],
        DATA.columns.to_list(), DATA.columns.to_list(),
    )

    # define components
    _class = {"sepal_length": "bg-light"}
    table_1 = ctable.layout(
        pathname, search, f"id-{TAG}-table2", DATA.to_dict("records")[:2],
        [], DATA.columns.to_list(), class_data=[_class, _class], striped=False, hover=False,
    )

    # return result
    return dbc.Card(children=[
        dbc.CardHeader(row_header, class_name="px-4 py-3"),
        html.Div([table_0, table_1], className="p-4"),
    ], class_name=None, style={"minHeight": "600px"})
