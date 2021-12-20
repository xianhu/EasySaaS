# _*_ coding: utf-8 _*_

"""
page of upload
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
# import dash_table
# import pandas as pd

from app import app

TAG = "upload"


def layout(pathname, search):
    """
    layout of page
    """
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col("Unknown file data", id=f"id-{TAG}-title", width="auto"),
            # dbc.Col(dcc.Upload(dbc.Button("Upload Data", size="sm"), id=f"id-{TAG}-upload0", accept=".csv,.xlsx", className="m-0"), width="auto"),
        ], align="center", justify="between", class_name="border-bottom mx-auto py-3"),
        # dbc.Row(dbc.Col(children=[
        #     # html.Img(src="assets/illustrations/upload.svg", className="img-fluid"),
        #     # dcc.Upload(dbc.Button("Upload Data", class_name="w-100 mt-4"), id=f"id-{TAG}-upload1", accept=".csv,.xlsx"),
        # ], width=10, md=3), id=f"id-{TAG}-content", align="center", justify="center", class_name="h-100-scroll w-100 mx-auto"),
    ], className="bg-white h-75 border rounded")


@app.callback([
    Output(f"id-{TAG}-title", "children"),
    Output(f"id-{TAG}-content", "children"),
], [
    Input(f"id-{TAG}-upload0", "filename"),
    # Input(f"id-{TAG}-upload1", "filename"),
    State(f"id-{TAG}-upload0", "contents"),
    # State(f"id-{TAG}-upload1", "contents"),
], prevent_initial_call=True)
def _button_click(filename0, contents0):
    print(filename0)
    return filename0, filename0
