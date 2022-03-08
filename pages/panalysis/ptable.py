# _*_ coding: utf-8 _*_

"""
table page
"""

import os

import flask_login
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dash_table, dcc

from app import app
from config import config_dir_store

TAG = "analysis-table"


def layout(pathname, search):
    """
    layout of page
    """
    user = flask_login.current_user

    # confirm and read file
    file_full_path = f"{config_dir_store}/{user.id}-{user.filename}"
    if not os.path.exists(file_full_path):
        file_full_path = "./assets/demo.csv"
    data = pd.read_csv(file_full_path, encoding="gbk")

    # define components
    args = {"size": "sm", "color": "primary", "outline": True}
    button = dbc.Button("Download file", id=f"id-{TAG}-button", **args)

    # return result
    return dbc.Card(children=[
        dcc.Download(id=f"id-{TAG}-download"),
        dcc.Store(id=f"id-{TAG}-filefp", data=file_full_path),
        dbc.Row(children=[
            dbc.Col(file_full_path, width="auto", class_name="fw-bold"),
            dbc.Col(button, width="auto", class_name=None),
        ], align="center", justify="between", class_name="border-bottom w-100 mx-auto px-3 py-2"),
        dbc.Row(dbc.Col(dash_table.DataTable(
            id=f"id-{TAG}-table",
            data=data.to_dict("records")[:100],
            columns=[{"name": str(i), "id": str(i)} for i in data.columns],
        ), width=12), align="start", justify="start", class_name="w-100 mx-auto px-3 py-3"),
    ], class_name="mt-2", style={"minHeight": "600px"})


@app.callback(Output(f"id-{TAG}-download", "data"), [
    Input(f"id-{TAG}-button", "n_clicks"),
    State(f"id-{TAG}-filefp", "data"),
], prevent_initial_call=True)
def _button_click(n_clicks, file_full_path):
    data = pd.read_csv(file_full_path, encoding="gbk")
    return dcc.send_data_frame(data.to_csv, "download.csv")
