# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app
from components import cnavbar, csmallnav, cadmulti, cadsingle
from utility import get_trigger_property
from . import pfileud
from .dplotly import pptbasic
from .dtables import ptbdash, ptbplotly

TAG = "analysis"
CATALOG_LIST = [
    ["Tables", f"id-{TAG}-ad-tables", [
        ("Dash Table", f"id-{TAG}-tb-dash", "#tb-dash"),
        ("Plotly Table", f"id-{TAG}-tb-plotly", "#tb-plotly"),
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
        cadmulti.layout(CATALOG_LIST, flush=True, class_name="border-bottom-solid"),
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
    ], className="d-flex flex-column vh-100 overflow-scroll")


@app.callback(output=[
    dict(
        cfileud=Output(f"id-{TAG}-fileud", "className"),
        ctbdash=Output(f"id-{TAG}-tb-dash", "className"),
        ctbplotly=Output(f"id-{TAG}-tb-plotly", "className"),
        cptbasic=Output(f"id-{TAG}-pt-basic", "className"),

    ),
    dict(
        is_open=Output(f"id-{TAG}-collapse", "is_open"),
        content=Output(f"id-{TAG}-content", "children"),
        href=Output({"type": "id-address", "index": TAG}, "href"),
    ),
], inputs=dict(
    n_clicks_temp=dict(
        n_clicks0=Input(f"id-{TAG}-fileud", "n_clicks"),
        n_clicks1=Input(f"id-{TAG}-tb-dash", "n_clicks"),
        n_clicks2=Input(f"id-{TAG}-tb-plotly", "n_clicks"),
        n_clicks3=Input(f"id-{TAG}-pt-basic", "n_clicks"),
    ),
    togger=dict(
        n_clicks=Input(f"id-{TAG}-toggler", "n_clicks"),
        is_open=State(f"id-{TAG}-collapse", "is_open"),
    ),
), prevent_initial_call=False)
def _init_page(n_clicks_temp, togger):
    # define class
    class_curr, class_none = "text-primary", "text-black hover-primary"

    # define output
    output0 = dict(
        cfileud=class_none, cptbasic=class_none,
        ctbdash=class_none, ctbplotly=class_none,
    )
    outpute = dict(is_open=dash.no_update, content=None, href=dash.no_update)

    # define variables
    triggered = dash.callback_context.triggered
    curr_id, _, _, value = get_trigger_property(triggered)

    # define is_open
    if curr_id == f"id-{TAG}-toggler" and togger["n_clicks"]:
        outpute.update(dict(is_open=(not togger["is_open"])))

    # define content
    curr_id = curr_id or f"id-{TAG}-fileud"
    if curr_id == f"id-{TAG}-fileud":
        output0.update(dict(cfileud=class_curr))
        outpute.update(dict(content=pfileud.layout(None, None)))

    # define content
    elif curr_id == f"id-{TAG}-tb-dash":
        output0.update(dict(ctbdash=class_curr))
        outpute.update(dict(
            is_open=False,
            content=ptbdash.layout(None, None),
        ))
    elif curr_id == f"id-{TAG}-tb-plotly":
        output0.update(dict(ctbplotly=class_curr))
        outpute.update(dict(
            is_open=False,
            content=ptbplotly.layout(None, None),
        ))

    # define content
    elif curr_id == f"id-{TAG}-pt-basic":
        output0.update(dict(cptbasic=class_curr))
        outpute.update(dict(
            is_open=False,
            content=pptbasic.layout(None, None),
        ))

    # return result
    return [output0, outpute]
