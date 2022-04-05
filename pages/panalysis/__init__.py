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
from .dplotly import pptbar, pptline, pptpie, pptscatter
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
    kwargs_file = dict(title="FileUp&Down", _id=f"id-{TAG}-fileud", path="#fileud")
    catalog = dbc.Collapse(children=[
        cadsingle.layout(**kwargs_file, flush=True, class_name="border-bottom-solid"),
        cadmulti.layout(CATALOG_LIST, flush=True, class_name="border-bottom-solid"),
    ], id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    ctid = f"id-{TAG}-content"
    content = dbc.Row(children=[
        dbc.Col(catalog, width=12, md=2, class_name="h-100-scroll-md bg-light"),
        dbc.Col(id=ctid, width=12, md=10, class_name="h-100-scroll mt-4 mt-md-0 p-md-4"),
    ], align="start", justify="center", class_name="h-100-scroll")

    # return result
    return html.Div(children=[
        cnavbar.layout(fluid=True, class_name=None),
        csmallnav.layout(f"id-{TAG}-toggler", "Analysis", fluid=True),
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
    class_curr_sigl = "text-primary"
    class_none_sigl = "text-black hover-primary"

    # define class
    class_curr_mult = "text-primary"
    class_none_mult = "text-black hover-primary"

    # define output
    output1 = dict(cfileud=class_none_sigl)
    output2 = dict(
        ctbdash=class_none_mult,
        ctbplotly=class_none_mult,
    )
    output3 = dict(
        cptscatter=class_none_mult,
        cptline=class_none_mult,
        cptbar=class_none_mult,
        cptpie=class_none_mult,
    )
    output4 = dict(content=None, href=None)

    # check user
    if not flask_login.current_user.is_authenticated:
        output4.update(dict(href=PATH_LOGOUT))
        return [output1, output2, output3, output4]

    # define content
    curr_id = (hvalue or "").strip("#") or "fileud"
    if curr_id == "fileud":
        output1.update(dict(cfileud=class_curr_sigl))
        output4.update(dict(content=pfileud.layout(None, None)))
    elif curr_id == "tb-dash":
        output2.update(dict(ctbdash=class_curr_mult))
        output4.update(dict(content=ptbdash.layout(None, None))),
    elif curr_id == "tb-plotly":
        output2.update(dict(ctbplotly=class_curr_mult))
        output4.update(dict(content=ptbplotly.layout(None, None))),
    elif curr_id == "pt-scatter":
        output3.update(dict(cptscatter=class_curr_mult))
        output4.update(dict(content=pptscatter.layout(None, None))),
    elif curr_id == "pt-line":
        output3.update(dict(cptline=class_curr_mult))
        output4.update(dict(content=pptline.layout(None, None))),
    elif curr_id == "pt-bar":
        output3.update(dict(cptbar=class_curr_mult))
        output4.update(dict(content=pptbar.layout(None, None))),
    elif curr_id == "pt-pie":
        output3.update(dict(cptpie=class_curr_mult))
        output4.update(dict(content=pptpie.layout(None, None))),

    # return result
    return [output1, output2, output3, output4]


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
