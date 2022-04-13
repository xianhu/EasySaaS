# _*_ coding: utf-8 _*_

"""
dash table page
"""

import dash_bootstrap_components as dbc
import plotly
from dash import Input, Output, dash_table, html

from app import app

TAG = "analysis-tables-dash"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return dbc.Card(children=[
        dbc.CardHeader("Dash Table", class_name="px-4 py-3"),
        html.Div(dbc.Spinner(id=f"id-{TAG}-content"), className="p-4"),
    ], class_name=None, style={"minHeight": "600px"})


@app.callback(
    Output(f"id-{TAG}-content", "children"),
    Input(f"id-{TAG}-content", "type"),
    prevent_initial_call=False,
)
def _init_page(spinner_type):
    data = plotly.data.iris()
    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict("records"),
        style_cell=dict(textAlign="left"),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender"),
    )
