# _*_ coding: utf-8 _*_

"""
catalog of page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..common import *
from ..paths import *

TAG = "mine"
CATALOG_LIST = [
    ("Profile", PATH_MINE_PROFILE),
    ("Upgrade", PATH_MINE_UPGRADE),
    ("Notify", PATH_MINE_NOTIFY),
]


def layout_catalog(pathname, search):
    """
    layout of catalog
    """
    # define class
    class_navlink0 = "fw-bold hover-primary text-muted"
    class_navlink1 = "fw-bold hover-primary"

    # define text
    cat_title, cat_list = "", []
    for title, path in CATALOG_LIST:
        if path != pathname:
            cat_list.append(dbc.NavLink(title, href=path, class_name=class_navlink0))
        else:
            cat_list.append(dbc.NavLink(title, href=path, class_name=class_navlink1))
            cat_title = f"My > {title}"
    cat_list.append(dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-100 mt-2"))

    # define component
    cat_toggler = dbc.NavbarToggler(COMP_I_LIST, id=f"id-{TAG}-toggler", class_name="border")

    # return result
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col(cat_title, width="auto", class_name="fw-bold text-primary"),
            dbc.Col(cat_toggler, width="auto", class_name=None),
        ], align="center", justify="between", class_name="d-md-none"),
        dbc.Collapse(cat_list, id=f"id-{TAG}-collapse", class_name="d-md-block")
    ], className=CLASS_DIV_CATALOG)


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
