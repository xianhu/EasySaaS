# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app
from . import ccatalog, pother, pplbasic, ptable
from ..components import cnavbar, csmallnav
from ..paths import PATH_ANALYSIS

TAG = "analysis"


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
    elif pathname == f"{PATH_ANALYSIS}-pl-basic":
        title = "Plotly Basic Page"
        content = pplbasic.layout(pathname, search)
    else:
        title = "Other Page"
        content = pother.layout(pathname, search)

    # define components
    catalog = ccatalog.layout(pathname, search, class_name=None)
    collapse = dbc.Collapse(catalog, id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    container = dbc.Row(children=[
        dbc.Col(collapse, width=12, md=2, class_name="h-100-scroll-md bg-light"),
        dbc.Col(content, width=12, md=10, class_name="h-100-scroll mt-4 mt-md-0 p-md-4"),
    ], align="start", justify="center", class_name="h-100-scroll")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=True, class_navbar=None),
        csmallnav.layout(pathname, search, f"id-{TAG}-toggler", title, fluid=True),
        dbc.Container(container, fluid=True, class_name="h-100-scroll"),
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
