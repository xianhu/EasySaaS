# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from app import app
from components import cfooter, cnavbar, ccatalog
from components import csmallnav
from utility import PATH_LOGOUT
from . import paccount, pbilling, padmin

TAG = "user"
CATALOG_LIST = [
    ["Admin", f"id-{TAG}-admin", "#admin"],
    ["ACCOUNT", None, [
        ("Info&Security", f"id-{TAG}-infosec", "#infosec"),
        ("Plan&Payments", f"id-{TAG}-planpay", "#planpay"),
    ]],
]


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    catalog = dbc.Collapse(dbc.Card(children=[
        ccatalog.layout(CATALOG_LIST, class_name=None),
        dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-2"),
    ], class_name="py-2"), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # return result
    return html.Div(children=[
        cnavbar.layout(fluid=False, class_name=None),
        csmallnav.layout(f"id-{TAG}-toggler", "User", fluid=False),
        dbc.Container(dbc.Row(children=[
            dbc.Col(catalog, width=12, md=2, class_name="mt-0 mt-md-4"),
            # dbc.Col(content, width=12, md=8, class_name="mt-4 mt-md-4"),
            dbc.Col(id=f"id-{TAG}-content", width=12, md=8, class_name="mt-4 mt-md-4"),
        ], align="start", justify="center"), fluid=False),
        cfooter.layout(fluid=False, class_name=None),
        dcc.Location(id=f"id-{TAG}-hash", refresh=False)
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


@app.callback(dict(
    content=Output(f"id-{TAG}-content", "children"),
    class_admin=Output(f"id-{TAG}-admin", "className"),
    class_infosec=Output(f"id-{TAG}-infosec", "className"),
    class_planpay=Output(f"id-{TAG}-planpay", "className"),
), Input(f"id-{TAG}-hash", "hash"), prevent_initial_call=False)
def _init_page(_hash):
    # define variables
    class_curr = "text-decoration-none px-4 py-2 text-primary"
    class_none = "text-decoration-none px-4 py-2 text-black hover-primary"
    outputs = dict(
        content=None,
        class_admin=class_none,
        class_infosec=class_none,
        class_planpay=class_none,
    )

    curr_id = f"id-{TAG}-{_hash.strip('#')}"
    if curr_id == f"id-{TAG}-admin":
        outputs["content"] = padmin.layout("", "")
        outputs["class_admin"] = class_curr
    elif curr_id == f"id-{TAG}-infosec":
        outputs["content"] = paccount.layout("", "")
        outputs["class_infosec"] = class_curr
    elif curr_id == f"id-{TAG}-planpay":
        outputs["content"] = pbilling.layout("", "")
        outputs["class_planpay"] = class_curr

    return outputs
