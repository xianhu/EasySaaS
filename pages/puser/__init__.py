# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from .. import palert
from ..paths import PATH_USER
from ..components import cfooter, cnavbar, csmallnav
from . import ccatalog, paccount, pbilling

TAG = "user"


def layout(pathname, search):
    """
    layout of page
    """
    # define pathname
    pathname = f"{PATH_USER}-general" if pathname == PATH_USER else pathname

    # define components
    if pathname == f"{PATH_USER}-general":
        title = " > ".join(["ACCOUNT", "General"])
        content = paccount.layout(pathname, search)
    elif pathname == f"{PATH_USER}-security":
        title = " > ".join(["ACCOUNT", "Security"])
        content = paccount.layout(pathname, search)
    elif pathname == f"{PATH_USER}-notifications":
        title = " > ".join(["ACCOUNT", "Notifications"])
        content = paccount.layout(pathname, search)
    elif pathname == f"{PATH_USER}-plan":
        title = " > ".join(["BILLING", "Plan"])
        content = pbilling.layout(pathname, search)
    elif pathname == f"{PATH_USER}-payments":
        title = " > ".join(["BILLING", "Payments"])
        content = pbilling.layout(pathname, search)
    else:
        return palert.layout_404(pathname, search, return_href=PATH_USER)

    # define components
    small_div = csmallnav.layout(pathname, search, f"id-{TAG}-toggler", title)
    collapse = dbc.Collapse(ccatalog.layout(pathname, search), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=None, class_navbar=None),
        dbc.Container(children=[small_div, dbc.Row(children=[
            dbc.Col(collapse, width=12, md=2, class_name="mt-0 mt-md-4"),
            dbc.Col(content, width=12, md=8, class_name="mt-4 mt-md-4"),
        ], justify="center", class_name="w-100 mx-auto")], class_name="p-0"),
        cfooter.layout(pathname, search, fluid=None, class_footer=None),
    ])


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
