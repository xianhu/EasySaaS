# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, dcc, html

from app import app
from components import cnavbar, csmallnav, cadmulti, cadsingle
from utility import PATH_LOGOUT, get_trigger_property
from . import pfileud
from .dplotly import pptbasic
from .dtables import ptbcustom, ptbdash

TAG = "analysis"
CATALOG_LIST = [
    ["Tables", f"id-{TAG}-ad-tables", [
        ("Dash Table", f"id-{TAG}-tb-dash", "#tb-dash"),
        ("Custom Table", f"id-{TAG}-tb-custom", "#tb-custom"),
    ]],
    ["Plotly", f"id-{TAG}-ad-plotly", [
        ("Basic Charts", f"id-{TAG}-pt-basic", "#pt-basic"),
    ]],
]


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define components
    kwargs_fileud = dict(title="FileUp&Down", _id=f"id-{TAG}-fileud", href="#fileud")
    catalog = dbc.Collapse(children=[
        cadsingle.layout(**kwargs_fileud, flush=True, class_name="border-bottom-solid"),
        cadmulti.layout(CATALOG_LIST, ad_id=f"id-{TAG}-ad", flush=True, class_name="border-bottom-solid"),
    ], id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    ctid = f"id-{TAG}-content"
    content = dbc.Row(children=[
        dbc.Col(catalog, width=12, md=2, class_name="h-100-scroll-md bg-light"),
        dbc.Col(id=ctid, width=12, md=10, class_name="h-100-scroll mt-4 mt-md-0 p-md-4"),
    ], align="start", justify="center", class_name="h-100-scroll")

    # return result
    tgid = f"id-{TAG}-toggler"
    return html.Div(children=[
        cnavbar.layout(fluid=True, class_name=None),
        csmallnav.layout(tgid, "Analysis", fluid=True, class_name=None),
        dbc.Container(content, fluid=True, class_name="h-100-scroll"),
        # define components
        html.A(id={"type": "id-address", "index": TAG}),
        dcc.Store(id=f"id-{TAG}-vhash", data=kwargs.get("vhash")),
        dcc.Store(id=f"id-{TAG}-dclient", data=kwargs.get("dclient")),
    ], className="d-flex flex-column vh-100 overflow-scroll")


@app.callback(output=[
    Output(f"id-{TAG}-ad", "active_item"),
    dict(
        fileud=Output(f"id-{TAG}-fileud", "className"),
        tbdash=Output(f"id-{TAG}-tb-dash", "className"),
        tbcustom=Output(f"id-{TAG}-tb-custom", "className"),
        ptbasic=Output(f"id-{TAG}-pt-basic", "className"),
    ),
    dict(
        is_open=Output(f"id-{TAG}-collapse", "is_open"),
        children=Output(f"id-{TAG}-content", "children"),
        href=Output({"type": "id-address", "index": TAG}, "href"),
    ),
], inputs=dict(
    n_clicks_temp=dict(
        n_clicks0=Input(f"id-{TAG}-fileud", "n_clicks"),
        n_clicks1=Input(f"id-{TAG}-tb-dash", "n_clicks"),
        n_clicks2=Input(f"id-{TAG}-tb-custom", "n_clicks"),
        n_clicks3=Input(f"id-{TAG}-pt-basic", "n_clicks"),
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
    output_active = dash.no_update
    output_class = dict(
        fileud=dash.no_update, tbdash=dash.no_update,
        tbcustom=dash.no_update, ptbasic=dash.no_update,
    )
    output_other = dict(is_open=dash.no_update, children=dash.no_update, href=dash.no_update)

    # check user
    if not flask_login.current_user.is_authenticated:
        output_other.update(dict(href=PATH_LOGOUT))
        return [output_active, output_class, output_other]

    # parse triggered
    triggered = dash.callback_context.triggered
    curr_id, _, _, value = get_trigger_property(triggered)

    # define is_open
    if curr_id == f"id-{TAG}-toggler" and togger["n_clicks"]:
        output_other.update(dict(is_open=(not togger["is_open"])))
        return [output_active, output_class, output_other]

    # define curr_id
    if (not curr_id) and vhash:
        curr_id = f"id-{TAG}-{vhash.strip('#')}"
    curr_id = curr_id or f"id-{TAG}-fileud"

    # define content
    if curr_id == f"id-{TAG}-fileud":
        output_class = dict(
            fileud=class_curr, tbdash=class_none,
            tbcustom=class_none, ptbasic=class_none,
        )
        output_other.update(dict(is_open=False, children=pfileud.layout(None, None)))

    # define content
    elif curr_id == f"id-{TAG}-tb-dash":
        output_active = f"id-{TAG}-ad-tables"
        output_class = dict(
            fileud=class_none, tbdash=class_curr,
            tbcustom=class_none, ptbasic=class_none,
        )
        output_other.update(dict(is_open=False, children=ptbdash.layout(None, None)))
    elif curr_id == f"id-{TAG}-tb-custom":
        output_active = f"id-{TAG}-ad-tables"
        output_class = dict(
            fileud=class_none, tbdash=class_none,
            tbcustom=class_curr, ptbasic=class_none,
        )
        output_other.update(dict(is_open=False, children=ptbcustom.layout(None, None)))

    # define content
    elif curr_id == f"id-{TAG}-pt-basic":
        output_active = f"id-{TAG}-ad-plotly"
        output_class = dict(
            fileud=class_none, tbdash=class_none,
            tbcustom=class_none, ptbasic=class_curr,
        )
        output_other.update(dict(is_open=False, children=pptbasic.layout(None, None)))

    # return result
    return [output_active, output_class, output_other]
