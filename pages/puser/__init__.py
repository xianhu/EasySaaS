# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, dcc, html

from app import app
from components import cfooter, cnavbar, csmallnav, ccatalog
from utility import PATH_LOGOUT
from . import padmin, pinfosec, pplanpay

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

    # define components
    ctid = f"id-{TAG}-content"
    content = dbc.Row(children=[
        dbc.Col(catalog, width=12, md=2, class_name="mt-0 mt-md-4"),
        dbc.Col(id=ctid, width=12, md=8, class_name="mt-4 mt-md-4"),
    ], align="start", justify="center", class_name=None)

    # return result
    return html.Div(children=[
        cnavbar.layout(fluid=False, class_name=None),
        csmallnav.layout(f"id-{TAG}-toggler", "User", fluid=False),
        dbc.Container(content, fluid=False, class_name=None),
        cfooter.layout(fluid=False, class_name=None),
        # define components
        html.A(id={"type": "id-address", "index": TAG}),
        dcc.Location(id=f"id-{TAG}-location", refresh=False),
    ], className="d-flex flex-column vh-100")


@app.callback(output=[
    dict(cadmin=Output(f"id-{TAG}-admin", "className")),
    dict(
        cinfosec=Output(f"id-{TAG}-infosec", "className"),
        cplanpay=Output(f"id-{TAG}-planpay", "className"),
    ),
    dict(
        content=Output(f"id-{TAG}-content", "children"),
        href=Output({"type": "id-address", "index": TAG}, "href"),
    ),
], inputs=Input(f"id-{TAG}-location", "hash"), prevent_initial_call=False)
def _init_page(hvalue):
    # define variables
    class_curr, class_none = "text-primary", "text-black hover-primary"

    # define output
    output1 = dict(cadmin=class_none)
    output2 = dict(
        cinfosec=class_none,
        cplanpay=class_none,
    )
    outpute = dict(content=None, href=None)

    # check user
    if not flask_login.current_user.is_authenticated:
        outpute.update(dict(href=PATH_LOGOUT))
        return [output1, output2, outpute]

    # define content
    curr_id = (hvalue or "").strip("#") or "infosec"
    if curr_id == "admin":
        output1.update(dict(cadmin=class_curr))
        outpute.update(dict(content=padmin.layout(None, None)))
    elif curr_id == "infosec":
        output2.update(dict(cinfosec=class_curr))
        outpute.update(dict(content=pinfosec.layout(None, None)))
    elif curr_id == "planpay":
        output2.update(dict(cplanpay=class_curr))
        outpute.update(dict(content=pplanpay.layout(None, None)))

    # return result
    return [output1, output2, outpute]


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    Input(f"id-{TAG}-location", "hash"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, hvalue, is_open):
    if n_clicks:
        return not is_open
    return is_open
