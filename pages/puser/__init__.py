# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from .. import palert
from ..paths import PATH_USER, PATH_LOGOUT
from ..components import cfooter, cnavbar, csmallnav
from . import paccount, pbilling

TAG = "user"
CATALOG_LIST = [
    ["ACCOUNT", None, [
        ("General", f"{PATH_USER}-general"),
        ("Security", f"{PATH_USER}-security"),
        ("Notifications", f"{PATH_USER}-notifications"),
    ]],
    ["BILLING", None, [
        ("Plan", f"{PATH_USER}-plan"),
        ("Payments", f"{PATH_USER}-payments"),
    ]],
]


def layout(pathname, search):
    """
    layout of page
    """
    # define pathname
    pathname = f"{PATH_USER}-general" if pathname == PATH_USER else pathname

    # define components
    cat_list = []
    class_first = "small text-muted mt-4 mb-2 px-4"
    class_second = "small text-decoration-none px-4 py-2"
    for title_first, icon_first, list_second in CATALOG_LIST:
        # define catalog list
        cat_list.append(html.Div(title_first, className=class_first))

        # define catalog list
        for title_second, path in list_second:
            _class = "text-black hover-primary" if path != pathname else "text-white bg-primary"
            cat_list.append(html.A(title_second, href=path, className=f"{class_second} {_class}"))
    cat_list.append(dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-4"))

    # define components
    if pathname == f"{PATH_USER}-general":
        title = " > ".join(["ACCOUNT", "general"])
        content = paccount.layout(pathname, search)
    elif pathname == f"{PATH_USER}-security":
        title = " > ".join(["ACCOUNT", "security"])
        content = paccount.layout(pathname, search)
    elif pathname == f"{PATH_USER}-notifications":
        title = " > ".join(["ACCOUNT", "notifications"])
        content = paccount.layout(pathname, search)
    elif pathname == f"{PATH_USER}-plan":
        title = " > ".join(["BILLING", "plan"])
        content = pbilling.layout(pathname, search)
    elif pathname == f"{PATH_USER}-payments":
        title = " > ".join(["BILLING", "payments"])
        content = pbilling.layout(pathname, search)
    else:
        return palert.layout_404(pathname, search, return_href=PATH_USER)

    # define components
    small_div = csmallnav.layout(pathname, search, f"id-{TAG}-toggler", title)
    catalog = dbc.Collapse(dbc.Card(cat_list), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=None, class_navbar=None),
        dbc.Container(children=[small_div, dbc.Row(children=[
            dbc.Col(catalog, width=12, md=2, class_name="mt-0 mt-md-4"),
            dbc.Col(content, width=12, md=8, class_name="mt-4 mt-md-4"),
        ], justify="center", class_name="w-100 mx-auto")], class_name="p-0"),
        cfooter.layout(pathname, search, fluid=None, class_footer=None),
    ])


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
