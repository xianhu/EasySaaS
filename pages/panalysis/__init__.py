# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, dcc, html

from components import cnavbar, csmallnav, cadmulti, cadsingle
from utility.paths import PATH_LOGOUT, NAV_LINKS
from .. import ptemplate

TAG = "analysis"

# catalog list
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
    kwargs_ad = dict(flush=True, class_name="border-catalog-bottom")
    catalog = dbc.Collapse(children=[
        cadsingle.layout("FileUp&Down", f"id-{TAG}-fileud", "#fileud", **kwargs_ad),
        cadmulti.layout(CATALOG_LIST, f"id-{TAG}-admulti", flush=True),
    ], id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    content = dbc.Row(children=[
        dbc.Col(children=catalog, width=12, md=2, class_name="h-100-scroll-md px-0 bg-dark"),
        dbc.Col(id=f"id-{TAG}-content", width=12, md=10, class_name="h-100-scroll mt-4 mt-md-0 p-md-4"),
    ], align="start", justify="center", class_name="h-100-scroll bg-light")

    # return result
    return html.Div(children=[
        # define components
        cnavbar.layout(NAV_LINKS, pathname, fluid=True, class_name=None),

        # define components
        csmallnav.layout(f"id-{TAG}-toggler", "Analysis", fluid=True),
        dbc.Container(content, fluid=True, class_name="h-100-scroll"),

        # define components
        # cfooter.layout(fluid=False, class_name=None),

        # define components
        html.A(id={"type": "id-address", "index": TAG}),

        # define components
        dcc.Store(id=f"id-{TAG}-pathname", data=pathname),
        dcc.Store(id=f"id-{TAG}-search", data=search),
        dcc.Store(id=f"id-{TAG}-vhash", data=kwargs.get("vhash")),
        dcc.Store(id=f"id-{TAG}-dclient", data=kwargs.get("dclient")),
    ], className="d-flex flex-column vh-100 overflow-auto")


@dash.callback(output=[
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
    Output(f"id-{TAG}-admulti", "active_item"),
], inputs=dict(
    n_clicks_list=dict(
        n_clicks0=Input(f"id-{TAG}-fileud", "n_clicks"),
        n_clicks1=Input(f"id-{TAG}-tb-dash", "n_clicks"),
        n_clicks2=Input(f"id-{TAG}-tb-custom", "n_clicks"),
        n_clicks3=Input(f"id-{TAG}-pt-basic", "n_clicks"),
    ),
    togger_dict=dict(
        n_clicks=Input(f"id-{TAG}-toggler", "n_clicks"),
        is_open=State(f"id-{TAG}-collapse", "is_open"),
    ),
    data_dict=dict(
        pathname=State(f"id-{TAG}-pathname", "data"),
        search=State(f"id-{TAG}-search", "data"),
        vhash=State(f"id-{TAG}-vhash", "data"),
        dclient=State(f"id-{TAG}-dclient", "data"),
    ),
), prevent_initial_call=False)
def _init_page(n_clicks_list, togger_dict, data_dict):
    # define default output
    output_class = dict(
        fileud=dash.no_update, tbdash=dash.no_update,
        tbcustom=dash.no_update, ptbasic=dash.no_update,
    )
    output_other = dict(is_open=dash.no_update, children=dash.no_update, href=dash.no_update)
    output_active = dash.no_update

    # check user login
    if not flask_login.current_user.is_authenticated:
        output_other.update(dict(href=PATH_LOGOUT))
        return [output_class, output_other, output_active]

    # define variables
    curr_id = dash.ctx.triggered_id
    pathname, search = data_dict.get("pathname"), data_dict.get("search")
    vhash, dclient = data_dict.get("vhash"), data_dict.get("dclient")

    # define is_open
    if curr_id == f"id-{TAG}-toggler" and togger_dict["n_clicks"]:
        output_other.update(dict(is_open=(not togger_dict["is_open"])))
        return [output_class, output_other, output_active]

    # define curr_id
    if (not curr_id) and vhash:
        curr_id = f"id-{TAG}-{vhash.strip('#').split('#')[0]}"
    curr_id = curr_id or f"id-{TAG}-fileud"

    # define content
    class_curr, class_none = dash.no_update, dash.no_update
    if curr_id == f"id-{TAG}-fileud":
        output_class = dict(fileud=class_curr, tbdash=class_none, tbcustom=class_none, ptbasic=class_none)
        output_other.update(dict(is_open=False, children=ptemplate.layout(pathname, search)))
        output_active = None
    elif curr_id == f"id-{TAG}-tb-dash":
        output_class = dict(fileud=class_none, tbdash=class_curr, tbcustom=class_none, ptbasic=class_none)
        output_other.update(dict(is_open=False, children=ptemplate.layout(pathname, search)))
        output_active = f"id-{TAG}-ad-tables"
    elif curr_id == f"id-{TAG}-tb-custom":
        output_class = dict(fileud=class_none, tbdash=class_none, tbcustom=class_curr, ptbasic=class_none)
        output_other.update(dict(is_open=False, children=ptemplate.layout(pathname, search)))
        output_active = f"id-{TAG}-ad-tables"
    elif curr_id == f"id-{TAG}-pt-basic":
        output_class = dict(fileud=class_none, tbdash=class_none, tbcustom=class_none, ptbasic=class_curr)
        output_other.update(dict(is_open=False, children=ptemplate.layout(pathname, search)))
        output_active = f"id-{TAG}-ad-plotly"
    else:
        raise Exception(f"Invalid curr_id: {curr_id}")

    # return result
    return [output_class, output_other, output_active]
