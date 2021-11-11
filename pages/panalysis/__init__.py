# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..comps import cfooter, cnavbar
from ..palert import *
from ..paths import *
from .config_cat import CATALOG_LIST

TAG = "analysis"


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    if pathname == PATH_ANALYSIS or pathname == f"{PATH_USER}-account":
        cat_title = "User > ACCOUNT"
        content_main = None
    elif pathname == f"{PATH_USER}-billing":
        cat_title = "User > BILLING"
        content_main = None
    else:
        return layout_404(pathname, search, PATH_USER)

    # define components
    cat_list = []
    for first_title, first_item in CATALOG_LIST:
        cat_list.append(html.Div(first_title, className="small text-muted mt-4 px-4"))

        for second_title, second_info in first_item:
            if second_info["href"]:
                cat_list.append(html.A(children=[
                    html.I(className=second_info["icon"]),
                    html.Div(second_title, className="ml-2")
                ]))
                print(first_title, second_title, second_info["href"])
                continue

            for third_title, third_path in second_info["items"]:
                cat_list.append(dbc.Accordion(children=[]))
                print(first_title, second_title, third_title, third_path)
        # if not path:
        #     class_cat = "small text-muted mt-4 px-4"
        #     cat_list.append(html.Div(title, className=class_cat))
        # else:
        #     class_cat = "small text-black hover-primary text-decoration-none mt-2 px-4"
        #     cat_list.append(html.A(title, href=path, className=class_cat))
    cat_list.append(dbc.Button("Logout", href=PATH_LOGOUT, class_name="w-75 mx-auto my-4"))

    # define components
    cat_icon = html.I(className="bi bi-list fs-1")
    cat_toggler = dbc.NavbarToggler(html.A(cat_icon), id=f"id-{TAG}-toggler", class_name="border")
    cat_collapse = dbc.Collapse(dbc.Card(cat_list), id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    content1 = dbc.Row(children=[
        dbc.Col(cat_title, width="auto", class_name="text-primary"),
        dbc.Col(cat_toggler, width="auto", class_name=None),
    ], align="center", justify="between", class_name="d-md-none w-100 mx-auto border-bottom py-2")

    # define components
    content2 = dbc.Row(children=[
        dbc.Col(cat_collapse, width=12, md=2, class_name=None),
        dbc.Col(content_main, width=12, md=8, class_name="mt-4 mt-md-0"),
    ], align="start", justify="center", class_name="w-100 mx-auto mt-0 mt-md-4")

    # define components
    navbar = cnavbar.layout(pathname, search, fluid=None)
    footer = cfooter.layout(pathname, search, fluid=None)

    # return result
    return [navbar, dbc.Container([content1, content2]), footer]


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
