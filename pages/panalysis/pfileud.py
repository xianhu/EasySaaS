# _*_ coding: utf-8 _*_

"""
file page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, html

from app import app

TAG = "analysis-fileud"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    return dbc.Card(children=[
        dbc.CardHeader("File Upload & Download", class_name="px-4 py-3"),
        html.Div(dbc.Spinner(id=f"id-{TAG}-content"), className="p-4"),
    ], class_name=None, style={"minHeight": "600px"})


@app.callback(
    Output(f"id-{TAG}-content", "children"),
    Input(f"id-{TAG}-content", "type"),
    prevent_initial_call=False,
)
def _init_page(spinner_type):
    return None
