# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..comps import cnavbar, csinglead, csmallnav
from ..paths import PATH_ANALYSIS
from . import pdesc, cupload

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
    upload_div = cupload.layout(pathname, search)
    white_gap = html.Div(style={"height": "4px"}, className="bg-light")

    cat_title, cat_list, active_id, content = None, [], None, None

    # define components
    href = f"{PATH_ANALYSIS}-table"
    button_children = html.A("Table", href=href, className="text-white text-decoration-none w-100")
    table = csinglead.layout(pathname, search, button_children, "accordion-bg bg-image-after-none", flush=True)
    if href == pathname:
        cat_title, content = "Table", "Table"

    # define components
    class_cat_second = "text-white text-decoration-none px-5 py-2"
    for first_cat_title, first_cat_icon, second_cat_list in CATALOG_LIST:
        item_id = f"id-{TAG}-{first_cat_title}"

        # define catalog
        ad_children = []
        for title, path in second_cat_list:
            _class = "accordion-bg-0" if path != pathname else "accordion-bg-1"
            ad_children.append(html.A(title, href=path, className=f"{class_cat_second} {_class}"))

            # define content
            if path == pathname:
                active_id = item_id
                cat_title = " > ".join([first_cat_title, title])
                content = " > ".join([first_cat_title, title])

        # define catalog list
        cat_list.append(dbc.AccordionItem(ad_children, item_id=item_id, title=first_cat_title))
    accordion = dbc.Accordion(cat_list, id=f"id-{TAG}-accordion", flush=True, active_item=active_id)

    # define components
    small_div = csmallnav.layout(pathname, search, f"id-{TAG}-toggler", cat_title)

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=True),
        dbc.Container(children=[small_div, dbc.Row(children=[
            dbc.Col(children=[
                dbc.Collapse([upload_div, white_gap, table, accordion], id=f"id-{TAG}-collapse", class_name="d-md-block"),
                html.Div("All rights reserved.", className="d-none d-md-block text-muted text-center mt-auto py-2"),
            ], width=12, md=2, class_name="d-flex flex-column accordion-bg h-100-scroll-md p-0"),
            dbc.Col(children=[
                html.Div(cat_title, className="d-none d-md-block text-muted my-2"),
                pdesc.layout(pathname, search),
            ], width=12, md=10, class_name="h-100-scroll px-md-4"),
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


