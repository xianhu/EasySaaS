# _*_ coding: utf-8 _*_

"""
analysis page
"""

import json

import dash
import dash_bootstrap_components as dbc
import feffery_utils_components as fuc
import flask_login
from dash import dcc, html, Input, Output, State, ALL

from components import cbrand
from utility.paths import PATH_LOGIN

TAG = "analysis1"
FMT_EXECUTEJS = """
    var nav_cur = document.getElementById('{nav_cur}');
    if (nav_cur) {{
        nav_cur.classList.remove('text-white');
        nav_cur.classList.add('text-success');
    }}    
    var ele_pre = document.getElementById('{nav_pre}');
    if (ele_pre) {{
        ele_pre.classList.remove('text-success');
        ele_pre.classList.add('text-white');
    }}
"""


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # user instance
    user = flask_login.current_user

    # define components
    class_link = "fs-6 text-white px-0 hover-success"
    navlink_list = [
        dbc.NavLink("Intros", id={"type": f"id-{TAG}-catalog", "index": "intros"}, href="#", class_name=class_link),
        dbc.NavLink("Products", id={"type": f"id-{TAG}-catalog", "index": "products"}, href="#", class_name=class_link),
        dbc.NavLink("Prices", id={"type": f"id-{TAG}-catalog", "index": "prices"}, href="#", class_name=class_link),
        dbc.NavLink("Contacts", id={"type": f"id-{TAG}-catalog", "index": "contacts"}, href="#", class_name=class_link),

        dbc.NavItem("HOME", class_name="small text-white-50 mt-4 mb-1"),
        dbc.NavLink("Overview", id={"type": f"id-{TAG}-catalog", "index": "hm-overview"}, href="#", class_name=class_link),
        dbc.NavLink("Updates", id={"type": f"id-{TAG}-catalog", "index": "hm-updates"}, href="#", class_name=class_link),
        dbc.NavLink("Reports", id={"type": f"id-{TAG}-catalog", "index": "hm-reports"}, href="#", class_name=class_link),

        dbc.NavItem("DASHBOARD", class_name="small text-white-50 mt-4 mb-1"),
        dbc.NavLink("Overview", id={"type": f"id-{TAG}-catalog", "index": "db-overview"}, href="#", class_name=class_link),
        dbc.NavLink("Weekly", id={"type": f"id-{TAG}-catalog", "index": "db-weekly"}, href="#", class_name=class_link),
        dbc.NavLink("Monthly", id={"type": f"id-{TAG}-catalog", "index": "db-monthly"}, href="#", class_name=class_link),
        dbc.NavLink("Annually", id={"type": f"id-{TAG}-catalog", "index": "db-annually"}, href="#", class_name=class_link),
    ]

    # define components
    id_profile = {"type": f"id-{TAG}-catalog", "index": "profile"}
    id_badge = {"type": f"id-{TAG}-catalog", "index": "badge"}
    navitem_bottom = dbc.NavItem(children=[
        dbc.DropdownMenu(children=[
            dbc.DropdownMenuItem("Profile", id=id_profile, href="#"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Logout", href=PATH_LOGIN),
        ], label=user.email.split("@")[0], class_name="me-1"),
        dbc.Badge(5, id=id_badge, color="danger", href="#", class_name="text-decoration-none"),
    ], class_name="d-flex align-items-center justify-content-start")

    # define components
    col_left = dbc.Col(children=[
        cbrand.layout(class_text=None, class_name=None),
        html.Hr(className="text-white my-2"),
        dbc.Nav(navlink_list, vertical=True, class_name="mb-auto"),
        html.Hr(className="text-white my-2"),
        dbc.Nav(navitem_bottom, vertical=True, class_name=None),
        # define components
        dcc.Store(id=f"id-{TAG}-navpre", data=None),
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
    ], width=12, md=2, class_name="bg-primary px-4 py-2 h-100-scroll d-flex flex-column")

    # define components
    col_right = dbc.Col(dbc.Spinner(children=[
        html.Div(id=f"id-{TAG}-content", className=None),
    ]), width=12, md=10, class_name="bg-light px-4 py-2 h-100-scroll")

    # return result
    return dbc.Row([col_left, col_right], class_name="bg-light vh-100 overflow-auto mx-0")


@dash.callback([
    Output(f"id-{TAG}-content", "children"),
    Output(f"id-{TAG}-navpre", "data"),
    Output(f"id-{TAG}-executejs", "jsString"),
], [
    Input({"type": f"id-{TAG}-catalog", "index": ALL}, "n_clicks"),
    State(f"id-{TAG}-navpre", "data"),
], prevent_initial_call=False)
def _update_content(n_clicks, nav_pre):
    # check trigger
    trigger_id = dash.ctx.triggered_id or {"index": "intros", "type": f"id-{TAG}-catalog"}
    nav_cur = json.dumps(trigger_id, separators=(",", ":"))

    # define variables
    if nav_cur.find("profile") >= 0 or nav_cur.find("badge") >= 0:
        nav_cur = ""
    js_string = FMT_EXECUTEJS.format(nav_pre=nav_pre, nav_cur=nav_cur)

    # return result
    return trigger_id["index"], nav_cur, js_string
