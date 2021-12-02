# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..comps import cnavbar
from ..palert import layout_404
from ..paths import *
from .catalog import CATALOG_LIST

TAG = "analysis"


def layout(pathname, search):
    """
    layout of page
    """
    if pathname == PATH_ANALYSIS:
        pathname = f"{PATH_ANALYSIS}-db-analytics"

    # define components
    cat_active_item = None
    cat_title, cat_list, cat_content = None, [], None
    for first_cat_title, first_cat_icon, second_cat_list in CATALOG_LIST:
        accordion_children, accordion_flag = [], False
        _class_0 = "text-white text-decoration-none px-5 py-2"
        for title, path in second_cat_list:
            if path == pathname:
                _class = f"{_class_0} accordion-bg-1"
            else:
                _class = f"{_class_0} accordion-bg-0"
            accordion_children.append(html.A(title, href=path, className=_class))

            # define content
            if path == pathname:
                cat_title = " > ".join([first_cat_title, title])
                cat_content = cat_title
                cat_active_item = f"id-{TAG}-{first_cat_title}"
        cat_list.append(dbc.AccordionItem(accordion_children, item_id=f"id-{TAG}-{first_cat_title}", title=first_cat_title))
    if (not cat_title) or (not cat_content):
        return layout_404(pathname, search, PATH_ANALYSIS)

    # define components
    cat_icon = html.I(className="bi bi-list fs-1")
    cat_toggler = dbc.NavbarToggler(html.A(cat_icon), id=f"id-{TAG}-toggler", class_name="border")
    cat_collapse = dbc.Collapse(children=[
        dbc.Accordion(cat_list, flush=True, active_item=cat_active_item, class_name=None),

    ], id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    content1 = dbc.Row(children=[
        dbc.Col(cat_title, width="auto", class_name="text-primary"),
        dbc.Col(cat_toggler, width="auto", class_name=None),
    ], align="center", justify="between", class_name="d-md-none border-bottom w-100 mx-auto py-2")

    # define components
    content2 = dbc.Row(children=[
        dbc.Col([
            cat_collapse,
            html.Div(children=[
                html.Div(["Powered by ©2021. All rights reserved."], className="text-white small text-center")
            ], className="mt-auto small-hidden"),
        ], width=12, md=2, class_name="h-100-scroll d-flex flex-column accordion-bg p-0"),
        dbc.Col(cat_content, width=12, md=10, class_name="mt-4 mt-md-0"),
    ], align="start", justify="center", class_name="h-100-scroll w-100 mx-auto mt-0")

    # define components
    navbar = cnavbar.layout(pathname, search, fluid=True)
    content = dbc.Container([content1, content2], fluid=True, class_name="h-100-scroll p-0")

    # return result
    return html.Div([navbar, content], className="d-flex flex-column vh-100 overflow-scroll")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
