# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..comps import cfooter, cnavbar
from ..palert import *
from ..paths import *
from . import paccount, pbilling

TAG = "user"

CATALOG_LIST = [
    ("ACCOUNT", None),
    ("General", f"{PATH_USER}-account"),
    ("Security", f"{PATH_USER}-account"),
    ("Notifications", f"{PATH_USER}-account"),

    ("BILLING", None),
    ("Plan", f"{PATH_USER}-billing"),
    ("Payments", f"{PATH_USER}-billing"),
]


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    if pathname == PATH_USER or pathname == f"{PATH_USER}-account":
        content = paccount.layout(pathname, search)
    elif pathname == f"{PATH_USER}-billing":
        content = pbilling.layout(pathname, search)
    else:
        return layout_404(pathname, search, PATH_USER)

    # define components
    cat_title, cat_list = "User > General", []
    for title, path in CATALOG_LIST:
        if not path:
            cat_list.append(html.Div(title, className=f"small text-muted {'mt-4' if cat_list else ''}"))
        else:
            cat_list.append(html.A(title, href=path, className="small text-black text-decoration-none, mt-2"))
        if path == pathname:
            cat_title = f"User > {title}"
    cat_list.append(dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-100 mt-4"))

    # define components
    cat_toggler = dbc.NavbarToggler(html.A(html.I(className="bi bi-list fs-1")), id=f"id-{TAG}-toggler", class_name="border")
    cat_collapse = dbc.Collapse(dbc.Card(cat_list, className="p-4"), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    fluid = None
    content1 = dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(cat_title, width="auto", class_name="fw-bold text-primary"),
            dbc.Col(cat_toggler, width="auto", class_name=None),
        ], align="center", justify="between", class_name="w-100 mx-auto"),
    ], fluid=fluid, class_name="d-md-none border-bottom py-2")
    content2 = dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(cat_collapse, width=12, md=2, class_name=None),
            dbc.Col(content, width=12, md=8, class_name="mt-4 mt-md-0"),
        ], align="start", justify="center", class_name="w-100 mx-auto"),
    ], fluid=fluid, class_name="mt-0 mt-md-4")

    # define components
    navbar = cnavbar.layout(pathname, search, fluid=fluid)
    footer = cfooter.layout(pathname, search, fluid=fluid)

    # return result
    return [navbar, content1, content2, footer]


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
