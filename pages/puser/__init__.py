# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app
from . import ccatalog
from .. import palert
from ..components import cfooter, cnavbar, csmallnav
from ..paths import PATH_USER

TAG = "user"


def layout(pathname, search):
    """
    layout of page
    """
    # define pathname
    pathname = f"{PATH_USER}-general" if pathname == PATH_USER else pathname

    # define components
    title, content = ccatalog.fcontent(pathname, search)
    if not content:
        return palert.layout_404(pathname, search, return_href=PATH_USER)

    # define components
    catalog = ccatalog.layout(pathname, search, class_name=None)
    collapse = dbc.Collapse(catalog, id=f"id-{TAG}-collapse", class_name="d-md-block")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=None, class_navbar=None),
        csmallnav.layout(pathname, search, f"id-{TAG}-toggler", title, fluid=None),
        dbc.Container(dbc.Row(children=[
            dbc.Col(collapse, width=12, md=2, class_name="mt-0 mt-md-4"),
            dbc.Col(content, width=12, md=8, class_name="mt-4 mt-md-4"),
        ], align="start", justify="center"), fluid=None),
        cfooter.layout(pathname, search, fluid=None, class_footer=None),
    ], className="d-flex flex-column vh-100")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
