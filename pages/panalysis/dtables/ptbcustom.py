# _*_ coding: utf-8 _*_

"""
custom table page
"""

import dash_bootstrap_components as dbc
import plotly
from dash import Input, Output, html

from app import app
from components import ctable

TAG = "analysis-tables-custom"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return dbc.Card(children=[
        dbc.CardHeader("Plotly Table", class_name="px-4 py-3"),
        dbc.Spinner(html.Div(id=f"id-{TAG}-content", className="p-4")),
    ], class_name=None, style={"minHeight": "600px"})


@app.callback(
    Output(f"id-{TAG}-content", "children"),
    Input(f"id-{TAG}-content", "className"),
    prevent_initial_call=False,
)
def _init_page(n_clicks):
    data = plotly.data.iris()

    # define table
    kwargs = dict(header_list=data.columns.to_list(), key_list=data.columns.to_list())
    table1 = ctable.layout(f"id-{TAG}-table1", data.to_dict("records")[:10], **kwargs)

    # define table
    _class = dict(sepal_length="bg-light")
    kwargs = dict(header_list=[], key_list=data.columns.to_list())
    kwargs.update(dict(class_data=[_class, _class], striped=False, hover=False))
    table2 = ctable.layout(f"id-{TAG}-table2", data.to_dict("records")[:2], **kwargs)

    # return result
    return html.Div(children=[table1, table2], className=None)
