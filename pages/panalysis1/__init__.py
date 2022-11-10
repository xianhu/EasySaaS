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
from utility.consts import FMT_EXECUTEJS_HREF
from utility.paths import PATH_LOGIN

TAG = "analysis1"
TAG_CAT = f"id-{TAG}-catalog"

# define jsString
FMT_EXECUTEJS = """
    var ele_cur = document.getElementById('{id_nav_cur}');
    if (ele_cur) {{
        ele_cur.classList.remove('text-white');
        ele_cur.classList.add('text-success');
    }}    
    var ele_pre = document.getElementById('{id_nav_pre}');
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
    vhash = kwargs.get("vhash")
    user = flask_login.current_user

    # define components
    class_link = "text-white hover-success px-0"
    navlink_list = [
        dbc.NavLink("Intros", id={"type": TAG_CAT, "index": "intros"}, href="#intros", class_name=class_link),
        dbc.NavLink("Products", id={"type": TAG_CAT, "index": "products"}, href="#products", class_name=class_link),
        dbc.NavLink("Prices", id={"type": TAG_CAT, "index": "prices"}, href="#prices", class_name=class_link),
        dbc.NavLink("Contacts", id={"type": TAG_CAT, "index": "contacts"}, href="#contacts", class_name=class_link),

        dbc.NavItem("HOME", class_name="small text-white-50 mt-4 mb-1"),
        dbc.NavLink("Overview", id={"type": TAG_CAT, "index": "hm-overview"}, href="#hm-overview", class_name=class_link),
        dbc.NavLink("Updates", id={"type": TAG_CAT, "index": "hm-updates"}, href="#hm-updates", class_name=class_link),
        dbc.NavLink("Reports", id={"type": TAG_CAT, "index": "hm-reports"}, href="#hm-reports", class_name=class_link),

        dbc.NavItem("DASHBOARD", class_name="small text-white-50 mt-4 mb-1"),
        dbc.NavLink("Overview", id={"type": TAG_CAT, "index": "db-overview"}, href="#db-overview", class_name=class_link),
        dbc.NavLink("Weekly", id={"type": TAG_CAT, "index": "db-weekly"}, href="#db-weekly", class_name=class_link),
        dbc.NavLink("Monthly", id={"type": TAG_CAT, "index": "db-monthly"}, href="#db-monthly", class_name=class_link),
        dbc.NavLink("Annually", id={"type": TAG_CAT, "index": "db-annually"}, href="#db-annually", class_name=class_link),
    ]

    # define components
    id_profile = {"type": TAG_CAT, "index": "profile"}
    id_badge = {"type": TAG_CAT, "index": "badge"}
    navitem_bottom = dbc.NavItem(children=[
        dbc.DropdownMenu(children=[
            dbc.DropdownMenuItem("Profile", id=id_profile, href="#profile"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Logout", href=PATH_LOGIN),
        ], align_end=False, label=user.email.split("@")[0], class_name="me-1"),
        dbc.Badge(5, id=id_badge, href="#badge", color="danger", class_name="text-decoration-none"),
    ], class_name="d-flex align-items-center justify-content-start")

    # define components
    col_left = dbc.Col(children=[
        cbrand.layout(class_text=None, class_name=None),
        html.Hr(className="text-white my-2"),
        dbc.Nav(navlink_list, vertical=True, class_name="mb-auto"),
        html.Hr(className="text-white my-2"),
        dbc.Nav(navitem_bottom, vertical=True, class_name=None),
        # define components
        dcc.Store(id=f"id-{TAG}-vhash", data=vhash),
        dcc.Store(id=f"id-{TAG}-navpre", data=None),
        fuc.FefferyExecuteJs(id=f"id-{TAG}-executejs"),
    ], width=2, class_name="d-flex flex-column vh-100 overflow-auto px-4 py-2 bg-primary")

    # define components
    col_right = dbc.Col(children=[
        html.Div(id=f"id-{TAG}-content", className=None),
    ], width=10, class_name="d-flex flex-column vh-100 overflow-auto px-4 py-2 bg-light")

    # return result
    return dbc.Row([col_left, col_right], class_name="vh-100 overflow-auto mx-0 bg-light")


@dash.callback([
    Output(f"id-{TAG}-navpre", "data"),
    Output(f"id-{TAG}-executejs", "jsString"),
    Output(f"id-{TAG}-content", "children"),
], [
    Input({"type": TAG_CAT, "index": ALL}, "n_clicks"),
    State(f"id-{TAG}-vhash", "data"),
    State(f"id-{TAG}-navpre", "data"),
], prevent_initial_call=False)
def _update_content(n_clicks, vhash, id_nav_pre):
    # check user
    user = flask_login.current_user
    if not user.is_authenticated:
        js_string = FMT_EXECUTEJS_HREF.format(href=PATH_LOGIN)
        return dash.no_update, js_string, dash.no_update

    # check trigger
    trigger_id = dash.ctx.triggered_id
    if not trigger_id:
        vhash = vhash.strip("#") or "intros"
        trigger_id = {"index": vhash, "type": TAG_CAT}

    # define variables
    id_nav_pre = id_nav_pre or ""
    id_nav_cur = "" if trigger_id["index"] in ("profile", "badge") else \
        json.dumps(trigger_id, separators=(",", ":"))
    js_string = FMT_EXECUTEJS.format(id_nav_pre=id_nav_pre, id_nav_cur=id_nav_cur)

    # define components
    content = trigger_id["index"]

    # return result
    return id_nav_cur, js_string, content
