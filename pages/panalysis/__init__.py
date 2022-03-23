# _*_ coding: utf-8 _*_

"""
analysis page
"""

import base64

import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc

from app import app
from components import cadmulti, cadsingle
from components import cnavbar, csmallnav
from config import config_dir_store
from paths import PATH_ANALYSIS
from templates import tnormal
from . import pother, pplotly, ptable

TAG = "analysis"
CATALOG_LIST = [
    ["Plotly", "bi bi-charts", [
        ("Scatter Plots", f"{PATH_ANALYSIS}-pl-scatter"),
        ("Line Charts", f"{PATH_ANALYSIS}-pl-line"),
        ("Bar Charts", f"{PATH_ANALYSIS}-pl-bar"),
        ("Pie Charts", f"{PATH_ANALYSIS}-pl-pie"),
    ]],
    ["Industry", "bi bi-charts", [
        ("Basic", f"{PATH_ANALYSIS}-id-basic"),
        ("Statistical", f"{PATH_ANALYSIS}-id-statistical"),
        ("Scientific", f"{PATH_ANALYSIS}-id-scientific"),
        ("Financial", f"{PATH_ANALYSIS}-id-financial"),
        ("AL And ML", f"{PATH_ANALYSIS}-id-alandml"),
    ]],
    ["Dashboards", "bi bi-house-door", [
        ("Analytics", f"{PATH_ANALYSIS}-db-analytics"),
        ("CustomRM", f"{PATH_ANALYSIS}-db-cumtomrm"),
        ("Ecommerce", f"{PATH_ANALYSIS}-db-ecommerce"),
        ("Projects", f"{PATH_ANALYSIS}-db-projects"),
    ]],
    ["Email", "bi bi-envelope", [
        ("Inbox", f"{PATH_ANALYSIS}-em-inbox"),
        ("Read Email", f"{PATH_ANALYSIS}-em-read"),
    ]],
    ["Project", "bi bi-cast", [
        ("List", f"{PATH_ANALYSIS}-pj-list"),
        ("Details", f"{PATH_ANALYSIS}-pj-details"),
        ("Gantt", f"{PATH_ANALYSIS}-pj-gantt"),
        ("Create Project", f"{PATH_ANALYSIS}-pj-create"),
    ]],
    ["Tasks", "bi bi-list-task", [
        ("List", f"{PATH_ANALYSIS}-ts-list"),
        ("Details", f"{PATH_ANALYSIS}-ts-details"),
        ("Kanban Board", f"{PATH_ANALYSIS}-ts-board"),
    ]],
]


def layout(pathname, search):
    """
    layout of page
    """
    # define pathname
    pathname = f"{PATH_ANALYSIS}-table" if pathname == PATH_ANALYSIS else pathname

    # define components
    if pathname == f"{PATH_ANALYSIS}-table":
        title = "Table Page"
        content = ptable.layout(pathname, search)
    elif pathname == f"{PATH_ANALYSIS}-pl-scatter":
        title = "Plotly Page"
        content = pplotly.layout(pathname, search, _type="scatter")
    elif pathname == f"{PATH_ANALYSIS}-pl-line":
        title = "Plotly Page"
        content = pplotly.layout(pathname, search, _type="line")
    elif pathname == f"{PATH_ANALYSIS}-pl-bar":
        title = "Plotly Page"
        content = pplotly.layout(pathname, search, _type="bar")
    elif pathname == f"{PATH_ANALYSIS}-pl-pie":
        title = "Plotly Page"
        content = pplotly.layout(pathname, search, _type="pie")
    else:
        title = "Other Page"
        content = pother.layout(pathname, search)

    # define components
    button = dbc.Button("Upload Data", class_name="w-75")
    args_up = {"accept": ".csv", "max_size": 1024 * 1024 * 10}

    # define components
    _class0 = "border-top-solid"
    _class1 = "border-top-solid border-bottom-solid"
    t_title, t_href = "Table", f"{PATH_ANALYSIS}-table"
    catalog = dbc.Collapse(children=[
        dcc.Upload(button, id=f"id-{TAG}-upload", **args_up, className="text-center my-4"),
        # cupload.layout(pathname, search, class_name="my-4"),
        cadsingle.layout(pathname, search, t_title, t_href, flush=True, class_name=_class0),
        cadmulti.layout(pathname, search, TAG, CATALOG_LIST, flush=True, class_name=_class1),
    ], id=f"id-{TAG}-collapse", class_name="d-md-block")

    # return result
    return tnormal.layout(pathname, search, TAG, children=[
        cnavbar.layout(pathname, search, fluid=True, class_navbar=None),
        csmallnav.layout(pathname, search, f"id-{TAG}-toggler", title, fluid=True),
        dbc.Container(dbc.Row(children=[
            dbc.Col(catalog, width=12, md=2, class_name="h-100-scroll-md bg-light"),
            dbc.Col(content, width=12, md=10, class_name="h-100-scroll mt-4 mt-md-0 p-md-4"),
        ], justify="center", class_name="h-100-scroll"), fluid=True, class_name="h-100-scroll"),
    ], class_name="d-flex flex-column vh-100 overflow-scroll")
    # return html.Div(children=, className=)


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


@app.callback(
    Output({"type": "id-address", "index": TAG}, "href"),
    Input(f"id-{TAG}-upload", "contents"),
    State(f"id-{TAG}-upload", "filename"),
    prevent_initial_call=True,
)
def _button_click(contents, filename):
    # store data
    content_type, content_string = contents.split(",")
    with open(f"{config_dir_store}/{filename}", "wb") as file_out:
        file_out.write(base64.b64decode(content_string))

    # return result
    return f"{PATH_ANALYSIS}-table"
