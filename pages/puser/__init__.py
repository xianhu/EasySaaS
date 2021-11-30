# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..comps import cfooter, cnavbar
from ..palert import layout_404
from ..paths import *

from .account import cbasic, cnofity, cpwd
from .billing import cinvoice, cplan

TAG = "user"

CATALOG_LIST = [
    ("ACCOUNT", None, None),
    ("General", f"{PATH_USER}-general", "ACCOUNT"),
    ("Security", f"{PATH_USER}-security", "ACCOUNT"),
    ("Notifications", f"{PATH_USER}-notifications", "ACCOUNT"),

    ("BILLING", None, None),
    ("Plan", f"{PATH_USER}-plan", "BILLING"),
    ("Payments", f"{PATH_USER}-payments", "BILLING"),
]


def layout(pathname, search):
    """
    layout of page
    """
    if pathname == PATH_USER:
        pathname = f"{PATH_USER}-general"

    # define components
    cat_list = []
    cat_title, content = None, None
    for title, path, parent in CATALOG_LIST:
        if not path:
            class_cat = "small text-muted mt-4 mb-2 px-4"
            cat_list.append(html.Div(title, className=class_cat))
            continue

        # define catlog
        if path == pathname:
            class_cat = "small text-white bg-primary text-decoration-none px-4 py-2"
        else:
            class_cat = "small text-black hover-primary text-decoration-none px-4 py-2"
        cat_list.append(html.A(title, href=path, className=class_cat))

        # define content
        if path == pathname:
            cat_title = " > ".join([parent, title])
            content = [
                cbasic.layout(pathname, search),
                cpwd.layout(pathname, search),
                cnofity.layout(pathname, search),
            ] if parent == "ACCOUNT" else [
                cplan.layout(pathname, search),
                cinvoice.layout(pathname, search),
            ]
    cat_list.append(dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-4"))

    # check and filter
    if (not cat_title) or (not content):
        return layout_404(pathname, search, PATH_USER)

    # define components
    cat_icon = html.I(className="bi bi-list fs-1")
    cat_toggler = dbc.NavbarToggler(html.A(cat_icon), id=f"id-{TAG}-toggler", class_name="border")
    cat_collapse = dbc.Collapse(dbc.Card(cat_list), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    content1 = dbc.Row(children=[
        dbc.Col(cat_title, width="auto", class_name="text-primary"),
        dbc.Col(cat_toggler, width="auto", class_name=None),
    ], align="center", justify="between", class_name="d-md-none w-100 border-bottom mx-auto py-2")

    # define components
    content2 = dbc.Row(children=[
        dbc.Col(cat_collapse, width=12, md=2, class_name=None),
        dbc.Col(content, width=12, md=8, class_name="mt-4 mt-md-0"),
    ], align="start", justify="center", class_name="w-100 mx-auto mt-0 mt-md-4")

    # define components
    navbar = cnavbar.layout(pathname, search, fluid=None)
    footer = cfooter.layout(pathname, search, fluid=None)

    # return result
    return html.Div([navbar, dbc.Container([content1, content2], class_name=None), footer], className=None)


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
