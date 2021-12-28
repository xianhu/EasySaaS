# _*_ coding: utf-8 _*_

"""
table page
"""

import os

import flask_login
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table, html

from config import config_dir_store


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
        id='table',
        columns=[{"name": str(i), "id": str(i)} for i in data.columns],
        data=data.to_dict('records'),
    )

    # return result
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col(f"File name: {file_name}", width="auto", class_name="fw-bold"),
            dbc.Col(dbc.Button("Download file", size="sm", color="primary", outline=True), width="auto"),
        ], align="center", justify="between", class_name="border-bottom w-100 mx-auto px-3 py-2"),
        dbc.Row(dbc.Col(content, width="auto"), align="start", justify="start", class_name="w-100 mx-auto p-3"),
    ], style={"min-height": "600px"})
