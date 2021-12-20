# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html

from app import app

from ..comps import cnavbar, csinglead, csmallnav
from ..paths import PATH_ANALYSIS
from .catalog import CATALOG_LIST
from . import pupload

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

    if cat_title == "Upload Data":
        cat_content = pupload.layout(pathname, search)

    # define components
    upload_div = html.Div(children=[
        dcc.Upload(children=[
            dbc.Button("Upload Data", class_name="w-75"),
        ], id=f"id-{TAG}-upload", accept=".csv,.xlsx", className="w-100 text-center"),
        html.Div(html.A("upload data documents", href="#", className="small text-muted"), className="text-center"),
    ], className="my-4")
    white_gap = html.Div(style={"height": "4px"}, className="bg-light")

    # define components
    _bc = html.A("Table", href="/", className="text-white text-decoration-none w-100")
    table = csinglead.layout(pathname, search, _bc, "accordion-bg accordion-button-after-none", {"border-bottom": "thin solid rgba(0, 0, 0, 0.5)"}, flush=True)
    # a = html.Div(html.Div(children=[
    #     html.H2(children=[
    #         html.Button(children=[
    #             ,
    #         ], className="accordion-button collapsed accordion-bg button-after-none"),
    #     ], className="accordion-header", style={"border-bottom": "thin solid rgba(0, 0, 0, 0.5)"}),
    # ], className="accordion-item"), className="accordion accordion-flush")

    # define components
    content = dbc.Row(children=[
        dbc.Col(children=[
            dbc.Collapse([upload_div, white_gap, table, accordion], id=f"id-{TAG}-collapse", class_name="d-md-block"),
            html.Div("All rights reserved.", className="d-none d-md-block text-muted text-center mt-auto py-2"),
        ], width=12, md=2, class_name="d-flex flex-column accordion-bg h-100-scroll-md p-0"),
        dbc.Col(children=[
            html.Div(cat_title, className="d-none d-md-block text-muted my-2"),
            cat_content,
            # html.Div(cat_content, className="bg-white h-75 border rounded mt-2"),
        ], width=12, md=10, class_name="h-100-scroll px-md-4"),
    ], justify="center", class_name="h-100-scroll w-100 mx-auto")

    # define components
    small_div = csmallnav.layout(pathname, search, cat_title, f"id-{TAG}-toggler")

    # return result
    return html.Div(children=[
        cnavbar.layout(pathname, search, fluid=True),
        dbc.Container([small_div, content], fluid=True, class_name="bg-light h-100-scroll p-0"),
        dcc.Store(id=f"id-{TAG}-filename"),
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


@app.callback([
    Output(f"id-{TAG}-filename", "data"),
], [
    Input(f"id-{TAG}-upload", "filename"),
    State(f"id-{TAG}-upload", "contents"),
], prevent_initial_call=True)
def _button_click(filename, contents):
    print(filename)
    return filename,
