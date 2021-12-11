# _*_ coding: utf-8 _*_

"""
user page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..comps import cfooter, cnavbar
from ..palert import layout_404
from ..paths import PATH_USER, PATH_LOGOUT

from .catalog import CATALOG_LIST
from .account import cbasic, cnofity, cpwd
from .billing import cinvoice, cplan

TAG = "user"


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    toggler_icon = html.A(html.I(className="bi bi-list fs-1"))
    pathname = f"{PATH_USER}-general" if pathname == PATH_USER else pathname

    # define components
    cat_title, cat_list, cat_content = None, [], None
    cat_class_first = "small text-muted mt-4 mb-2 px-4"
    cat_class_second = "small text-decoration-none px-4 py-2"
    for first_cat_title, first_cat_icon, second_cat_list in CATALOG_LIST:
        # define catlog list
        cat_list.append(html.Div(first_cat_title, className=cat_class_first))

        # define catlog list
        for title, path in second_cat_list:
            _class = "text-black hover-primary" if path != pathname else "text-white bg-primary"
            cat_list.append(html.A(title, href=path, className=f"{cat_class_second} {_class}"))

            # define content
            if path == pathname:
                cat_title = " > ".join([first_cat_title, title])
                if first_cat_title == "ACCOUNT":
                    cat_content = [
                        cbasic.layout(pathname, search),
                        cpwd.layout(pathname, search),
                        cnofity.layout(pathname, search),
                    ]
                if first_cat_title == "BILLING":
                    cat_content = [
                        cplan.layout(pathname, search),
                        cinvoice.layout(pathname, search),
                    ]
    # define catlog list
    cat_list.append(dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-4"))
    if (not cat_title) or (not cat_content):
        return layout_404(pathname, search, return_href=PATH_USER)

    # define components
    content = dbc.Row(children=[
        dbc.Col(children=[
            dbc.Collapse(dbc.Card(cat_list), id=f"id-{TAG}-collapse", class_name="d-md-block"),
        ], width=12, md=2, class_name="mt-0 mt-md-4"),
        dbc.Col(cat_content, width=12, md=8, class_name="mt-4 mt-md-4"),
    ], justify="center", class_name="w-100 mx-auto")

    # define components
    small_div = dbc.Row(children=[
        dbc.Col(cat_title, width="auto", class_name="text-primary"),
        dbc.Col(dbc.NavbarToggler(toggler_icon, id=f"id-{TAG}-toggler", class_name="border"), width="auto"),
    ], align="center", justify="between", class_name="d-md-none border-bottom w-100 mx-auto py-2")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=None),
        dbc.Container([small_div, content], class_name="p-0"),
        cfooter.layout(pathname, search, fluid=None),
    ], className="bg-light")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
