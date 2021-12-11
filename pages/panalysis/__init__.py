# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..comps import cnavbar
from ..paths import PATH_ANALYSIS
from .catalog import CATALOG_LIST

TAG = "analysis"


def layout(pathname, search):
    """
    layout of page
    """
    # define components
    toggler_icon = html.A(html.I(className="bi bi-list fs-1"))
    pathname = f"{PATH_ANALYSIS}-upload" if pathname == PATH_ANALYSIS else pathname

    # define components
    cat_list, cat_active_id = [], None
    cat_title, cat_content = "Upload Data", "Upload Data"
    cat_class_second = "text-white text-decoration-none px-5 py-2"
    for first_cat_title, first_cat_icon, second_cat_list in CATALOG_LIST:
        item_id = f"id-{TAG}-{first_cat_title}"

        # define catalog
        ad_children = []
        for title, path in second_cat_list:
            _class = "accordion-bg-0" if path != pathname else "accordion-bg-1"
            ad_children.append(html.A(title, href=path, className=f"{cat_class_second} {_class}"))

            # define content
            if path == pathname:
                cat_active_id = item_id
                cat_title = " > ".join([first_cat_title, title])
                cat_content = " > ".join([first_cat_title, title])

        # define catalog list
        cat_list.append(dbc.AccordionItem(ad_children, item_id=item_id, title=first_cat_title))
    accordion = dbc.Accordion(cat_list, id=f"id-{TAG}-accordion", flush=True, active_item=cat_active_id)

    # define components
    upload_div = html.Div(children=[
        dbc.Button("Upload Data", href=f"{PATH_ANALYSIS}-upload", class_name="w-75"),
        html.A("upload data documents", href="#", className="small text-muted"),
    ], className="d-flex flex-column align-items-center my-4")
    white_gap = html.Div(style={"height": "4px"}, className="bg-light")

    # define components
    content = dbc.Row(children=[
        dbc.Col(children=[
            dbc.Collapse([upload_div, white_gap, accordion], id=f"id-{TAG}-collapse", class_name="d-md-block"),
            html.Div("All rights reserved.", className="small-hidden text-muted text-center mt-auto py-2"),
        ], width=12, md=2, class_name="d-flex flex-column accordion-bg h-100-scroll-md p-0"),
        dbc.Col(children=[
            html.Div(cat_title, className="d-none d-md-block text-muted mt-2"),
            html.Div(cat_content, className="bg-white border rounded mt-2", style={"min-height": "75%"}),
        ], width=12, md=10, class_name="h-100-scroll px-md-4"),
    ], justify="center", class_name="h-100-scroll w-100 mx-auto")

    # define components
    small_div = dbc.Row(children=[
        dbc.Col(cat_title, width="auto", class_name="text-primary"),
        dbc.Col(dbc.NavbarToggler(toggler_icon, id=f"id-{TAG}-toggler", class_name="border"), width="auto"),
    ], align="center", justify="between", class_name="d-md-none border-bottom w-100 mx-auto py-2")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=True),
        dbc.Container([small_div, content], fluid=True, class_name="h-100-scroll p-0"),
    ], className="d-flex flex-column bg-light vh-100 overflow-scroll")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
