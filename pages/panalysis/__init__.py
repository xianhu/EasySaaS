# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from .. import palert
from ..paths import PATH_ANALYSIS
from ..components import cnavbar, csinglead, csmallnav
from . import cupload, pother, ptable

TAG = "analysis"
CATALOG_LIST = [
    ["Plotly", "bi bi-charts", [
        ("Basic", f"{PATH_ANALYSIS}-pl-basic"),
        ("Statistical", f"{PATH_ANALYSIS}-pl-statistical"),
        ("Scientific", f"{PATH_ANALYSIS}-pl-scientific"),
        ("Financial", f"{PATH_ANALYSIS}-pl-financial"),
        ("AL And ML", f"{PATH_ANALYSIS}-pl-alandml"),
    ]],
    ["Dashboards", "bi bi-house-door", [
        ("Analytics", f"{PATH_ANALYSIS}-db-analytics"),
        ("CustomRM", f"{PATH_ANALYSIS}-db-cumtomrm"),
        ("Ecommerce", f"{PATH_ANALYSIS}-db-ecommerce"),
        ("Projects", f"{PATH_ANALYSIS}-db-projects"),
    ]],
    ["Email", "bi bi-envelope", [
        ("Inbox", f"{PATH_ANALYSIS}-em-inbox"),
        ("Read Email", f"{PATH_ANALYSIS}-em-read"),
    ]],
    ["Project", "bi bi-cast", [
        ("List", f"{PATH_ANALYSIS}-pj-list"),
        ("Details", f"{PATH_ANALYSIS}-pj-details"),
        ("Gantt", f"{PATH_ANALYSIS}-pj-gantt"),
        ("Create Project", f"{PATH_ANALYSIS}-pj-create"),
    ]],
    ["Tasks", "bi bi-list-task", [
        ("List", f"{PATH_ANALYSIS}-ts-list"),
        ("Details", f"{PATH_ANALYSIS}-ts-details"),
        ("Kanban Board", f"{PATH_ANALYSIS}-ts-board"),
    ]],
]


def layout(pathname, search):
    """
    layout of page
    """
    # define pathname
    pathname = f"{PATH_ANALYSIS}-table" if pathname == PATH_ANALYSIS else pathname

    # define components
    cat_list, active_id = [], None
    class_second = "text-decoration-none px-5 py-2"
    for index, (title_first, icon_first, list_second) in enumerate(CATALOG_LIST):
        item_id = f"id-{TAG}-accordion-{index}"

        # define ad_children
        ad_children = []
        for title_second, path in list_second:
            # define active_id
            if path == pathname:
                active_id = item_id

            # define ad_children
            _class = "text-black hover-primary" if path != pathname else ""
            ad_children.append(html.A(title_second, href=path, className=f"{class_second} {_class}"))

        # define catalog list
        _class = "border-bottom-solid" if index == len(CATALOG_LIST) - 1 else ""
        cat_list.append(dbc.AccordionItem(ad_children, item_id=item_id, title=title_first, class_name=_class))

    # define components
    if pathname == f"{PATH_ANALYSIS}-table":
        title = "Table"
        content = ptable.layout(pathname, search)
    elif pathname.startswith(PATH_ANALYSIS):
        title = "Other page"
        content = pother.layout(pathname, search)
    else:
        return palert.layout_404(pathname, search, return_href=PATH_ANALYSIS)

    # define components
    ad_id, ad_title, ad_class, ad_href = f"id-{TAG}-sad1", "Table", "bg-light", f"{PATH_ANALYSIS}-table"
    small_div = csmallnav.layout(pathname, search, f"id-{TAG}-toggler", title)
    collapse = dbc.Collapse(children=[
        cupload.layout(pathname, search),
        csinglead.layout(pathname, search, ad_id, ad_title, ad_class, ad_href, flush=True),
        dbc.Accordion(cat_list, id=f"id-{TAG}-accordion", active_item=active_id, flush=True),
    ], id=f"id-{TAG}-collapse", class_name="d-md-block")
    footer = html.Div("All rights reserved.", className="d-none d-md-block text-muted text-center mt-auto py-2")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=True, class_navbar=None),
        dbc.Container(children=[small_div, dbc.Row(children=[
            dbc.Col([collapse, footer], width=12, md=2, class_name="d-flex flex-column bg-light h-100-scroll-md p-0"),
            dbc.Col(dbc.Card(content, class_name="mt-2"), width=12, md=10, class_name="h-100-scroll px-md-4"),
        ], justify="center", class_name="h-100-scroll w-100 mx-auto")], fluid=True, class_name="h-100-scroll p-0"),
    ], className="d-flex flex-column vh-100 overflow-scroll")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
