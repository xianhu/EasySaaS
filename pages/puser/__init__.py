# _*_ coding: utf-8 _*_

"""
user page
"""

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, dcc, html

from app import app
from components import cfooter, cnavbar, csmallnav, ccatalog
from utility import PATH_LOGOUT, get_trigger_property
from . import ptemplate, pinfosec, pplanpay

TAG = "user"
CATALOG_LIST = [
    ["Template", f"id-{TAG}-template", "#template"],
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
    tgid = f"id-{TAG}-toggler"
    return html.Div(children=[
        # define components
        cnavbar.layout(fluid=False, class_name=None),
        csmallnav.layout(tgid, "User", fluid=False, class_name=None),
        # define components
        dbc.Container(content, fluid=False, class_name=None),
        # define components
        cfooter.layout(fluid=False, class_name=None),
        # define components
        html.A(id={"type": "id-address", "index": TAG}),
        dcc.Store(id=f"id-{TAG}-vhash", data=kwargs.get("vhash")),
        dcc.Store(id=f"id-{TAG}-dclient", data=kwargs.get("dclient")),
    ], className="d-flex flex-column vh-100 overflow-scroll")


@app.callback(output=[
    dict(
        template=Output(f"id-{TAG}-template", "className"),
        infosec=Output(f"id-{TAG}-infosec", "className"),
        planpay=Output(f"id-{TAG}-planpay", "className"),
    ),
    dict(
        is_open=Output(f"id-{TAG}-collapse", "is_open"),
        children=Output(f"id-{TAG}-content", "children"),
        href=Output({"type": "id-address", "index": TAG}, "href"),
    ),
], inputs=dict(
    n_clicks_temp=dict(
        n_clicks0=Input(f"id-{TAG}-template", "n_clicks"),
        n_clicks1=Input(f"id-{TAG}-infosec", "n_clicks"),
        n_clicks2=Input(f"id-{TAG}-planpay", "n_clicks"),
    ),
    togger=dict(
        n_clicks=Input(f"id-{TAG}-toggler", "n_clicks"),
        is_open=State(f"id-{TAG}-collapse", "is_open"),
    ),
    vhash=State(f"id-{TAG}-vhash", "data"),
    dclient=State(f"id-{TAG}-dclient", "data"),
), prevent_initial_call=False)
def _init_page(n_clicks_temp, togger, vhash, dclient):
    # define class
    class_curr, class_none = "text-primary", "text-black hover-primary"

    # define default output
    output_class = dict(template=dash.no_update, infosec=dash.no_update, planpay=dash.no_update)
    output_other = dict(is_open=dash.no_update, children=dash.no_update, href=dash.no_update)

    # check user
    if not flask_login.current_user.is_authenticated:
        output_other.update(dict(href=PATH_LOGOUT))
        return [output_class, output_other]

    # parse triggered
    triggered = dash.callback_context.triggered
    curr_id, _, _, value = get_trigger_property(triggered)

    # define is_open
    if curr_id == f"id-{TAG}-toggler" and togger["n_clicks"]:
        output_other.update(dict(is_open=(not togger["is_open"])))
        return [output_class, output_other]

    # define curr_id
    if (not curr_id) and vhash:
        curr_id = f"id-{TAG}-{vhash.strip('#')}"
    curr_id = curr_id or f"id-{TAG}-infosec"

    # define content
    if curr_id == f"id-{TAG}-template":
        output_class = dict(template=class_curr, infosec=class_none, planpay=class_none)
        output_other.update(dict(is_open=False, children=ptemplate.layout(None, None)))
    elif curr_id == f"id-{TAG}-infosec":
        output_class = dict(template=class_none, infosec=class_curr, planpay=class_none)
        output_other.update(dict(is_open=False, children=pinfosec.layout(None, None)))
    elif curr_id == f"id-{TAG}-planpay":
        output_class = dict(template=class_none, infosec=class_none, planpay=class_curr)
        output_other.update(dict(is_open=False, children=pplanpay.layout(None, None)))

    # return result
    return [output_class, output_other]
