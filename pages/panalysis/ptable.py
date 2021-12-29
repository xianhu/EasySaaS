# _*_ coding: utf-8 _*_

"""
table page
"""

import os

import flask_login
import pandas
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, dash_table, dcc, html

from app import app
from config import config_dir_store

TAG = "analysis-table"


def layout(pathname, search):
    """
    layout of page
    """
    user = flask_login.current_user

    # confirm file
    file_name = user.filename
    file_full_path = f"{config_dir_store}/{user.id}-{user.filename}"
    if not os.path.exists(file_full_path):
        file_name = "demo.csv"
        file_full_path = "./assets/demo.csv"

    # read file
    if file_name.endswith(".csv"):
        data = pd.read_csv(file_full_path, encoding="gbk")
    else:
        data = pd.read_excel(file_full_path)

    # define components
    content = dash_table.DataTable(
        id=f"id-{TAG}-table",
        columns=[{"name": str(i), "id": str(i)} for i in data.columns],
        data=data.to_dict("records")[:100],
    )

    # return result
    args = {"size": "sm", "color": "primary", "outline": True}
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col(f"File name: {file_name}", width="auto", class_name="fw-bold"),
            dbc.Col(dbc.Button("Download file", id=f"id-{TAG}-button", **args), width="auto"),
        ], align="center", justify="between", class_name="border-bottom w-100 mx-auto px-3 py-2"),
        dbc.Row(dbc.Col(content, width=12), align="start", justify="start", class_name="w-100 mx-auto p-3"),
        dcc.Download(id=f"id-{TAG}-download"),
    ], style={"minHeight": "600px"})


@app.callback(
    Output(f"id-{TAG}-download", "data"),
    Input(f"id-{TAG}-button", "n_clicks"),
    prevent_initial_call=True,
)
def _button_click(n_clicks):
    df = pandas.read_csv("./assets/demo.csv", encoding="gbk")
    return dcc.send_data_frame(df.to_csv, "demo.csv")
