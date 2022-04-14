# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, dcc, html

from app import app
from components import cnavbar, csmallnav, cadmulti, cadsingle
from utility import PATH_LOGOUT
from . import pfileud
from .dplotly import ppttemplate
from .dtables import ptbdash, ptbplotly

TAG = "analysis"
CATALOG_LIST = [
    ["Tables", f"id-{TAG}-ad-tables", [
        ("Dash Table", f"id-{TAG}-tb-dash", "#tb-dash"),
        ("Plotly Table", f"id-{TAG}-tb-plotly", "#tb-plotly"),
    ]],
    ["Plotly", f"id-{TAG}-ad-plotly", [
        ("Scatter Charts", f"id-{TAG}-pt-scatter", "#pt-scatter"),
        ("Line Charts", f"id-{TAG}-pt-line", "#pt-line"),
        ("Bar Charts", f"id-{TAG}-pt-bar", "#pt-bar"),
        ("Pie Charts", f"id-{TAG}-pt-pie", "#pt-pie"),
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
        dcc.Location(id=f"id-{TAG}-location", refresh=False),
    ], className="d-flex flex-column vh-100 overflow-scroll")


@app.callback(output=[
    dict(cfileud=Output(f"id-{TAG}-fileud", "className")),
    dict(
        ctbdash=Output(f"id-{TAG}-tb-dash", "className"),
        ctbplotly=Output(f"id-{TAG}-tb-plotly", "className"),
    ),
    dict(
        cptscatter=Output(f"id-{TAG}-pt-scatter", "className"),
        cptline=Output(f"id-{TAG}-pt-line", "className"),
        cptbar=Output(f"id-{TAG}-pt-bar", "className"),
        cptpie=Output(f"id-{TAG}-pt-pie", "className"),
    ),
    dict(
        content=Output(f"id-{TAG}-content", "children"),
        href=Output({"type": "id-address", "index": TAG}, "href"),
    ),
], inputs=Input(f"id-{TAG}-location", "hash"), prevent_initial_call=False)
def _init_page(hvalue):
    # define class
    class_curr = "text-primary"
    class_none = "text-black hover-primary"

    # define output
    output1 = dict(cfileud=class_none)
    output2 = dict(ctbdash=class_none, ctbplotly=class_none)
    output3 = dict(
        cptscatter=class_none, cptline=class_none,
        cptbar=class_none, cptpie=class_none,
    )
    outpute = dict(content=None, href=None)

    # check user
    if not flask_login.current_user.is_authenticated:
        outpute.update(dict(href=PATH_LOGOUT))
        return [output1, output2, output3, outpute]

    # define content
    curr_id = (hvalue or "").strip("#") or "fileud"
    if curr_id == "fileud":
        output1.update(dict(cfileud=class_curr))
        outpute.update(dict(content=pfileud.layout(None, None)))

    # define content
    elif curr_id == "tb-dash":
        output2.update(dict(ctbdash=class_curr))
        outpute.update(dict(content=ptbdash.layout(None, None)))
    elif curr_id == "tb-plotly":
        output2.update(dict(ctbplotly=class_curr))
        outpute.update(dict(content=ptbplotly.layout(None, None)))

    # define content(ppttemplate)
    elif curr_id == "pt-scatter":
        output3.update(dict(cptscatter=class_curr))
        outpute.update(dict(content=ppttemplate.layout(None, None)))
    elif curr_id == "pt-line":
        output3.update(dict(cptline=class_curr))
        outpute.update(dict(content=ppttemplate.layout(None, None)))
    elif curr_id == "pt-bar":
        output3.update(dict(cptbar=class_curr))
        outpute.update(dict(content=ppttemplate.layout(None, None)))
    elif curr_id == "pt-pie":
        output3.update(dict(cptpie=class_curr))
        outpute.update(dict(content=ppttemplate.layout(None, None)))

    # return result
    return [output1, output2, output3, outpute]


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
