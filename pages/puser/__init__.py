# _*_ coding: utf-8 _*_

"""
user page
"""

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import Input, Output, State, dcc, html

from components import cfooter, cnavbar, ccatalog
from utility.paths import PATH_LOGOUT, NAV_LINKS
from . import pinfosec
from .. import ptemplate

TAG = "user"

# catalog list
CATALOG_LIST = [
    ["Notifications", f"id-{TAG}-notify", "#notify"],
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
        ccatalog.layout(catalog_list=CATALOG_LIST, class_name=None),
        dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-2"),
    ], class_name="py-2"), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    content = dbc.Row(children=[
        dbc.Col(children=catalog, width=12, md=2),
        dbc.Col(id=f"id-{TAG}-content", width=12, md=8),
    ], align="start", justify="center", class_name="my-4")

    # return result
    return html.Div(children=[
        # define components
        cnavbar.layout(NAV_LINKS, pathname, fluid=False),
        dbc.Container(children=content, fluid=False),
        cfooter.layout(fluid=False, class_name=None),

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
        notify=Output(f"id-{TAG}-notify", "className"),
        infosec=Output(f"id-{TAG}-infosec", "className"),
        planpay=Output(f"id-{TAG}-planpay", "className"),
    ),
    dict(
        children=Output(f"id-{TAG}-content", "children"),
        href=Output({"type": "id-address", "index": TAG}, "href"),
    ),
], inputs=dict(
    n_clicks_list=dict(
        n_clicks0=Input(f"id-{TAG}-notify", "n_clicks"),
        n_clicks1=Input(f"id-{TAG}-infosec", "n_clicks"),
        n_clicks2=Input(f"id-{TAG}-planpay", "n_clicks"),
    ),
    data_dict=dict(
        pathname=State(f"id-{TAG}-pathname", "data"),
        search=State(f"id-{TAG}-search", "data"),
        vhash=State(f"id-{TAG}-vhash", "data"),
        dclient=State(f"id-{TAG}-dclient", "data"),
    ),
), prevent_initial_call=False)
def _init_page(n_clicks_list, data_dict):
    # define default output
    output_class = dict(notify=dash.no_update, infosec=dash.no_update, planpay=dash.no_update)
    output_other = dict(children=dash.no_update, href=dash.no_update)

    # check user login
    if not flask_login.current_user.is_authenticated:
        output_other.update(dict(href=PATH_LOGOUT))
        return [output_class, output_other]

    # define variables
    pathname, search = data_dict.get("pathname"), data_dict.get("search")
    vhash, dclient = data_dict.get("vhash"), data_dict.get("dclient")

    # define curr_id
    curr_id = dash.ctx.triggered_id
    if (not curr_id) and vhash:
        curr_id = f"id-{TAG}-{vhash.strip('#').split('#')[0]}"
    curr_id = curr_id or f"id-{TAG}-infosec"

    # define content
    class_none = "text-decoration-none py-2 text-black hover-success"
    class_curr = "text-decoration-none py-2 text-success hover-success"
    if curr_id == f"id-{TAG}-notify":
        output_class = dict(notify=class_curr, infosec=class_none, planpay=class_none)
        output_other.update(dict(children=ptemplate.layout(pathname, search)))
    elif curr_id == f"id-{TAG}-infosec":
        output_class = dict(notify=class_none, infosec=class_curr, planpay=class_none)
        output_other.update(dict(children=pinfosec.layout(pathname, search)))
    elif curr_id == f"id-{TAG}-planpay":
        output_class = dict(notify=class_none, infosec=class_none, planpay=class_curr)
        output_other.update(dict(children=ptemplate.layout(pathname, search)))
    else:
        raise Exception(f"Invalid curr_id: {curr_id}")

    # return result
    return [output_class, output_other]
