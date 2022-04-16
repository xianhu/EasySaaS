# _*_ coding: utf-8 _*_

"""
file page
"""

import base64

import dash_bootstrap_components as dbc
import plotly
from dash import Input, Output, State, dcc, html

from app import app

TAG = "analysis-fileud"


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    button_up = dbc.Button("Upload Data", id=f"id-{TAG}-btnup")
    upload = dcc.Upload(button_up, id=f"id-{TAG}-upload", max_size=1024 * 1024 * 10)

    # define components
    button_down = dbc.Button("Download Data", id=f"id-{TAG}-btndown")
    download = dcc.Download(id=f"id-{TAG}-download", data=None, base64=None),

    # return result
    return dbc.Card(children=[
        dbc.CardHeader("File Upload & Download", class_name="px-4 py-3"),
        html.Div(children=[
            dbc.Row(children=[
                dbc.Col(upload, width="auto"),
                dbc.Col(download, width="auto"),
                dbc.Col(button_down, width="auto"),
            ], class_name="mb-2"),
            html.Div(id=f"id-{TAG}-content"),
        ], className="p-4"),
    ], class_name=None, style={"minHeight": "600px"})


@app.callback(
    Output(f"id-{TAG}-content", "children"),
    Input(f"id-{TAG}-upload", "contents"),
    State(f"id-{TAG}-upload", "filename"),
    prevent_initial_call=True,
)
def _button_click(contents, filename):
    # check data
    if not (contents and filename):
        return "no file"

    # upload data
    content_type, content_string = contents.split(",")
    with open(f".data/{filename}", "wb") as file_out:
        file_out.write(base64.b64decode(content_string))

    # return result
    return filename


@app.callback(
    Output(f"id-{TAG}-download", "data"),
    Input(f"id-{TAG}-btndown", "n_clicks"),
    prevent_initial_call=True,
)
def _button_click(n_clicks):
    # download data
    data = plotly.data.iris()
    # return dcc.send_data_frame(data.to_csv, filename="demo.csv", sep="\t", index=False)
    return dict(base64=False, filename="demo.csv", content=data.to_csv(sep="\t", index=False))
