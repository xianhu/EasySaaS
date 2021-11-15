# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..comps import cfooter, cnavbar
from ..palert import *
from ..paths import *
from . import catalog

TAG = "analysis"


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    if pathname == PATH_ANALYSIS:
        cat_title = "Analysis"
        content_main = ""
    elif pathname == f"{PATH_ANALYSIS}-db-analytics":
        cat_title = "-db-analytics"
        content_main = "-db-analytics"
    else:
        return layout_404(pathname, search, PATH_USER)

    # define components
    cat_icon = html.I(className="bi bi-list fs-1")
    cat_toggler = dbc.NavbarToggler(html.A(cat_icon), id=f"id-{TAG}-toggler", class_name="border")
    cat_collapse = dbc.Collapse(html.Div(catalog.layout(pathname, search)), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    content1 = dbc.Row(children=[
        dbc.Col(cat_title, width="auto", class_name="text-primary"),
        dbc.Col(cat_toggler, width="auto", class_name=None),
    ], align="center", justify="between", class_name="d-md-none w-100 mx-auto border-bottom py-2")

    # define components
    content2 = dbc.Row(children=[
        dbc.Col(cat_collapse, width=12, md=2, class_name="h-100 overflow-scroll bg-dark1 text-white p-0"),
        dbc.Col(content_main, width=12, md=10, class_name="mt-4 mt-md-0"),
    ], align="start", justify="center", class_name="w-100 mx-auto p-0 mt-0 h-100")

    # define components
    navbar = cnavbar.layout(pathname, search, fluid=True)
    footer = cfooter.layout(pathname, search, fluid=True)

    # return result
    return html.Div([navbar, dbc.Container([content2], fluid=True, class_name="p-0 h-100 overflow-scroll")], className="vh-100 overflow-scroll d-flex flex-column")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
