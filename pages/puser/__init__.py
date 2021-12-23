# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..comps import cfooter, cnavbar, csmallnav
from ..palert import layout_404
from ..paths import PATH_USER, PATH_LOGOUT

from . import account, billing

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
    # define pathname and class
    pathname = f"{PATH_USER}-general" if pathname == PATH_USER else pathname
    class_cat_first = "small text-muted mt-4 mb-2 px-4"
    class_cat_second = "small text-decoration-none px-4 py-2"

    # define components
    cat_title, cat_list, content = None, [], None
    for first_cat_title, first_cat_icon, second_cat_list in CATALOG_LIST:
        # define catlog list
        cat_list.append(html.Div(first_cat_title, className=class_cat_first))

        # define catlog list
        for title, path in second_cat_list:
            _class = "text-black hover-primary" if path != pathname else "text-white bg-primary"
            cat_list.append(html.A(title, href=path, className=f"{class_cat_second} {_class}"))

            # define content
            if path == pathname:
                cat_title = " > ".join([first_cat_title, title])
                if first_cat_title == "ACCOUNT":
                    content = account.layout(pathname, search)
                if first_cat_title == "BILLING":
                    content = billing.layout(pathname, search)
    # define catlog list
    cat_list.append(dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-4"))
    if (not cat_title) or (not content):
        return layout_404(pathname, search, return_href=PATH_USER)

    # define components
    small_div = csmallnav.layout(pathname, search, f"id-{TAG}-toggler", cat_title)
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
