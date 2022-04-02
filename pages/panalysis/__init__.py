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
from paths import PATH_ANALYSIS
from templates import tnormal
from . import pplotly, ptable

TAG = "analysis"
CATALOG_LIST = [
    ["Plotly", f"id-{TAG}-ad-plotly", [
        ("Scatter Plots", f"id-{TAG}-pl-scatter", f"{PATH_ANALYSIS}-pl-scatter"),
        ("Line Charts", f"id-{TAG}-pl-line", f"{PATH_ANALYSIS}-pl-line"),
        ("Bar Charts", f"id-{TAG}-pl-bar", f"{PATH_ANALYSIS}-pl-bar"),
        ("Pie Charts", f"id-{TAG}-pl-pie", f"{PATH_ANALYSIS}-pl-pie"),
    ]],
    ["Industry", f"id-{TAG}-ad-industry", [
        ("Basic", f"id-{TAG}-id-basic", f"{PATH_ANALYSIS}-id-basic"),
        ("Statistical", f"id-{TAG}-id-statistical", f"{PATH_ANALYSIS}-id-statistical"),
        ("Scientific", f"id-{TAG}-id-scientific", f"{PATH_ANALYSIS}-id-scientific"),
        ("Financial", f"id-{TAG}-id-financial", f"{PATH_ANALYSIS}-id-financial"),
        ("AL And ML", f"id-{TAG}-id-alandml", f"{PATH_ANALYSIS}-id-alandml"),
    ]],
    ["Dashboards", f"id-{TAG}-ad-dashboards", [
        ("Analytics", f"id-{TAG}-db-analytics", f"{PATH_ANALYSIS}-db-analytics"),
        ("CustomRM", f"id-{TAG}-db-cumtomrm", f"{PATH_ANALYSIS}-db-cumtomrm"),
        ("Ecommerce", f"id-{TAG}-db-ecommerce", f"{PATH_ANALYSIS}-db-ecommerce"),
        ("Projects", f"id-{TAG}-db-projects", f"{PATH_ANALYSIS}-db-projects"),
    ]],
    ["Email", f"id-{TAG}-ad-email", [
        ("Inbox", f"id-{TAG}-em-inbox", f"{PATH_ANALYSIS}-em-inbox"),
        ("Read Email", f"id-{TAG}-em-read", f"{PATH_ANALYSIS}-em-read"),
    ]],
    ["Project", f"id-{TAG}-ad-project", [
        ("List", f"id-{TAG}-pj-list", f"{PATH_ANALYSIS}-pj-list"),
        ("Details", f"id-{TAG}-pj-details", f"{PATH_ANALYSIS}-pj-details"),
        ("Gantt", f"id-{TAG}-pj-gantt", f"{PATH_ANALYSIS}-pj-gantt"),
        ("Create Project", f"id-{TAG}-pj-create", f"{PATH_ANALYSIS}-pj-create"),
    ]],
    ["Tasks", f"id-{TAG}-ad-tasks", [
        ("List", f"id-{TAG}-ts-list", f"{PATH_ANALYSIS}-ts-list"),
        ("Details", f"id-{TAG}-ts-details", f"{PATH_ANALYSIS}-ts-details"),
        ("Kanban Board", f"id-{TAG}-ts-board", f"{PATH_ANALYSIS}-ts-board"),
    ]],
]


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define pathname
    pathname = f"{PATH_ANALYSIS}-table" if pathname == PATH_ANALYSIS else pathname

    # define components
    if pathname.startswith(f"{PATH_ANALYSIS}-pl-"):
        title = "Plotly Page"
        content = pplotly.layout(pathname, search, _type=pathname.split("-")[-1])
    else:
        title = "Table Page"
        content = ptable.layout(pathname, search)

    # define components
    button = dbc.Button("Upload Data", class_name="w-75")
    args_up = {"accept": ".csv", "max_size": 1024 * 1024 * 10}
    t_title, t_id, t_href = "Table", f"id-{TAG}-table", f"{PATH_ANALYSIS}-table"

    # define components
    catalog = dbc.Collapse(children=[
        dcc.Upload(button, id=f"id-{TAG}-upload", **args_up, className="text-center my-4"),
        cadsingle.layout(t_title, t_id, t_href, curr_path=pathname, flush=True, class_name="border-top-solid"),
        cadmulti.layout(CATALOG_LIST, flush=True, class_name="border-top-solid border-bottom-solid"),
    ], id=f"id-{TAG}-collapse", class_name="d-md-block")

    # return result
    return tnormal.layout(pathname, search, TAG, children=[
        cnavbar.layout(fluid=True, class_name=None),
        csmallnav.layout(f"id-{TAG}-toggler", title, fluid=True),
        dbc.Container(dbc.Row(children=[
            dbc.Col(catalog, width=12, md=2, class_name="h-100-scroll-md bg-light"),
            dbc.Col(content, width=12, md=10, class_name="h-100-scroll mt-4 mt-md-0 p-md-4"),
        ], justify="center", class_name="h-100-scroll"), fluid=True, class_name="h-100-scroll"),
    ], class_name="d-flex flex-column vh-100 overflow-scroll")


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
    with open(f".data/{filename}", "wb") as file_out:
        file_out.write(base64.b64decode(content_string))

    # return result
    return f"{PATH_ANALYSIS}-table"
