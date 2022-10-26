# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash
import dash_bootstrap_components as dbc
import flask_login
from dash import html, Input, Output, ALL

from components import cbrand
from utility.paths import PATH_LOGIN

TAG = "analysis1"


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
    navitem_bottom = dbc.NavItem(children=[
        dbc.DropdownMenu(children=[
            dbc.DropdownMenuItem("Basic Profile", id=f"id-{TAG}-profile", href="#"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Logout", href=PATH_LOGIN),
        ], label=user.email.split("@")[0], class_name="me-1"),
        dbc.Badge(5, id=f"id-{TAG}-badge", color="danger", href="#", class_name="text-decoration-none"),
    ], class_name="d-flex align-items-center justify-content-start")

    # define components
    col_left = dbc.Col(children=[
        cbrand.layout(class_text=None, class_name=None),
        html.Hr(className="text-white my-2"),
        dbc.Nav(navlink_list, vertical=True, class_name="mb-auto"),
        html.Hr(className="text-white my-2"),
        dbc.Nav(navitem_bottom, vertical=True, class_name=None),
    ], width=12, md=2, class_name="bg-primary px-4 py-2 h-100-scroll d-flex flex-column")

    # define components
    col_right = dbc.Col(children=[
        dbc.Container("analysis page", id=f"id-{TAG}-content", fluid=True),
    ], width=12, md=10, class_name="bg-light px-4 py-2 h-100-scroll")

    # return result
    return dbc.Row([col_left, col_right], class_name="bg-light vh-100 overflow-auto mx-0")


@dash.callback(
    Output(f"id-{TAG}-content", "children"),
    Input({"type": f"id-{TAG}-catalog", "index": ALL}, "n_clicks"),
    prevent_initial_call=False,
)
def _update_content(n_clicks):
    # check trigger
    trigger = dash.ctx.triggered_id
    trigger_index = trigger["index"] if trigger else "intros"

    # return result
    return trigger_index
