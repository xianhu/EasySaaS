# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from .. import palert
from ..paths import PATH_ANALYSIS
from ..components import cnavbar, csmallnav
from . import ccatalog, pother, ptable

TAG = "analysis"


def layout(pathname, search):
    """
    layout of page
    """
    # define pathname
    pathname = f"{PATH_ANALYSIS}-table" if pathname == PATH_ANALYSIS else pathname

    # define components
    if pathname == f"{PATH_ANALYSIS}-table":
        title = "Table"
        content = ptable.layout(pathname, search)
    elif pathname.startswith(PATH_ANALYSIS):
        title = "Other page"
        content = pother.layout(pathname, search)
    else:
        return palert.layout_404(pathname, search, return_href=PATH_ANALYSIS)

    # define components
    catalog = ccatalog.layout(pathname, search, class_name=None)
    collapse = dbc.Collapse(catalog, id=f"id-{TAG}-collapse", class_name="d-md-block")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=True, class_navbar=None),
        csmallnav.layout(pathname, search, f"id-{TAG}-toggler", title, fluid=True),
        dbc.Container(dbc.Row(children=[
            dbc.Col(collapse, width=12, md=2, class_name="bg-light h-100-scroll-md"),
            dbc.Col(content, width=12, md=10, class_name="h-100-scroll px-md-4 py-md-3"),
        ], justify="center", class_name="h-100-scroll w-100 mx-auto"), fluid=True, class_name="h-100-scroll p-0"),
    ], className="d-flex flex-column vh-100 overflow-scroll")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
