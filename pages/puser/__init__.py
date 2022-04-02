# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app
from components import cfooter, cnavbar, csmallnav, ccatalog
from consts import PATH_LOGOUT, PATH_USER
from . import paccount, pbilling

TAG = "user"
CATALOG_LIST = [
    ["Admin", f"id-{TAG}-admin", f"{PATH_USER}-admin"],
    ["ACCOUNT", None, [
        ("General", f"id-{TAG}-ac-general", f"{PATH_USER}-ac-general"),
        ("Security", f"id-{TAG}-ac-security", f"{PATH_USER}-ac-security"),
        ("Notifications", f"id-{TAG}-ac-notify", f"{PATH_USER}-ac-notify"),
    ]],
    ["BILLING", None, [
        ("Plan", f"id-{TAG}-bl-plan", f"{PATH_USER}-bl-plan"),
        ("Payments", f"id-{TAG}-bl-payments", f"{PATH_USER}-bl-payments"),
    ]],
]


def layout(pathname, search, **kwargs):
    """
    layout of page
    """
    # define pathname
    pathname = f"{PATH_USER}-ac-general" if pathname == PATH_USER else pathname

    # define components
    if pathname.startswith(f"{PATH_USER}-bl-"):
        title = "BILLING"
        content = pbilling.layout(pathname, search, title=title)
    else:
        title = "ACCOUNT"
        content = paccount.layout(pathname, search, title=title)

    # define components
    catalog = dbc.Collapse(dbc.Card(children=[
        ccatalog.layout(CATALOG_LIST, curr_path=pathname, class_name=None),
        dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-2"),
    ], class_name="py-2"), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # return result
    return html.Div(children=[
        cnavbar.layout(fluid=False, class_name=None),
        csmallnav.layout(f"id-{TAG}-toggler", title, fluid=False),
        dbc.Container(dbc.Row(children=[
            dbc.Col(catalog, width=12, md=2, class_name="mt-0 mt-md-4"),
            dbc.Col(content, width=12, md=8, class_name="mt-4 mt-md-4"),
        ], align="start", justify="center"), fluid=False),
        cfooter.layout(fluid=False, class_name=None),
    ], className="d-flex flex-column vh-100")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
