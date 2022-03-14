# _*_ coding: utf-8 _*_

"""
table page
"""

import os

import dash_bootstrap_components as dbc
import flask_login
import pandas as pd
from dash import Input, Output, State, dash_table, dcc, html

from app import app
from config import config_dir_store

TAG = "analysis-table"


def layout(pathname, search):
    """
    layout of page
    """
    user = flask_login.current_user

    # confirm and read file
    file_path = f"{config_dir_store}/{user.id}-{user.filename}"
    if not os.path.exists(file_path):
        file_path = "./assets/demo.csv"

    # define components
    args = {"size": "sm", "color": "primary", "outline": True}
    button = dbc.Button("Download File", id=f"id-{TAG}-button", **args)

    # define components
    row_header = dbc.Row(children=[
        dbc.Col(file_path, width="auto"),
        dbc.Col(button, width="auto"),
    ], align="center", justify="between")

    # return result
    data = pd.read_csv(file_path, encoding="gbk")
    return dbc.Card(children=[
        dcc.Download(id=f"id-{TAG}-download"),
        dcc.Store(id=f"id-{TAG}-filepath", data=file_path),
        dbc.CardHeader(row_header, class_name="px-4 py-3"),
        html.Div(dash_table.DataTable(
            id=f"id-{TAG}-table",
            data=data.to_dict("records")[:100],
            columns=[{"name": str(i), "id": str(i)} for i in data.columns],
        ), className="p-4"),
    ], class_name=None, style={"minHeight": "600px"})


@app.callback(
    Output(f"id-{TAG}-download", "data"),
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-filepath", "data"),
    prevent_initial_call=True,
)
def _button_click(n_clicks, file_path):
    data = pd.read_csv(file_path, encoding="gbk")
    return dcc.send_data_frame(data.to_csv, "download.csv")
