# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app
from . import cupload, pother, pplotly, ptable
from ..components1 import cnavbar, csmallnav
from ..components2 import cadmulti, cadsingle
from ..paths import PATH_ANALYSIS

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
    t_title, t_href = "Table", f"{PATH_ANALYSIS}-table"
    _class0, _class1 = "border-top-solid", "border-top-solid border-bottom-solid"
    catalog = dbc.Collapse(children=[
        cupload.layout(pathname, search, class_name="my-4"),
        cadsingle.layout(pathname, search, t_title, t_href, flush=True, class_name=_class0),
        cadmulti.layout(pathname, search, TAG, CATALOG_LIST, flush=True, class_name=_class1),
    ], id=f"id-{TAG}-collapse", class_name="d-md-block")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=True, class_navbar=None),
        csmallnav.layout(pathname, search, f"id-{TAG}-toggler", title, fluid=True),
        dbc.Container(dbc.Row(children=[
            dbc.Col(catalog, width=12, md=2, class_name="h-100-scroll-md bg-light"),
            dbc.Col(content, width=12, md=10, class_name="h-100-scroll mt-4 mt-md-0 p-md-4"),
        ], justify="center", class_name="h-100-scroll"), fluid=True, class_name="h-100-scroll"),
    ], className="d-flex flex-column vh-100 overflow-scroll")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
