# _*_ coding: utf-8 _*_

"""
analysis page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..comps import cnavbar
from ..palert import layout_404
from ..paths import PATH_ANALYSIS

from .catalog import CATALOG_LIST

TAG = "analysis"


def layout(pathname, search):
    """
    layout of page
    """
    # change pathname
    if pathname == PATH_ANALYSIS:
        pathname = f"{PATH_ANALYSIS}-db-analytics"

    # define components
    cat_active_item = None
    cat_title, cat_list, cat_content = None, [], None
    cat_class_second = "text-white text-decoration-none px-5 py-2"
    for first_cat_title, first_cat_icon, second_cat_list in CATALOG_LIST:
        a_children = []
        for title, path in second_cat_list:
            # define catlog list
            _class = "accordion-bg-0" if path != pathname else "accordion-bg-1"
            a_children.append(html.A(title, href=path, className=f"{cat_class_second} {_class}"))

            # define content
            if path == pathname:
                cat_active_item = f"id-{TAG}-{first_cat_title}"
                cat_title = " > ".join([first_cat_title, title])
                cat_content = " > ".join([first_cat_title, title])

        # define catlog list
        item_id = f"id-{TAG}-{first_cat_title}"
        cat_list.append(dbc.AccordionItem(a_children, item_id=item_id, title=first_cat_title))
    if (not cat_title) or (not cat_content):
        return layout_404(pathname, search, PATH_ANALYSIS)

    # define components
    cat_icon = html.I(className="bi bi-list fs-1")
    cat_toggler = dbc.NavbarToggler(html.A(cat_icon), id=f"id-{TAG}-toggler", class_name="border")

    # define components
    collapse_item = dbc.Accordion(cat_list, flush=True, active_item=cat_active_item)
    cat_collapse = dbc.Collapse(collapse_item, id=f"id-{TAG}-collapse", class_name="d-md-block")

    # define components
    cat_footer = html.Div(children=[
        "Powered by ©2021. All rights reserved."
    ], className="small small-hidden text-white text-center mt-auto")

    # define components
    content1 = dbc.Row(children=[
        dbc.Col(cat_title, width="auto", class_name="text-primary"),
        dbc.Col(cat_toggler, width="auto", class_name=None),
    ], align="center", justify="between", class_name="d-md-none border-bottom w-100 mx-auto py-2")

    # define components
    class_catlog = "d-flex flex-column accordion-bg h-100-scroll p-0"
    content2 = dbc.Row(children=[
        dbc.Col([cat_collapse, cat_footer], width=12, md=2, class_name=class_catlog),
        dbc.Col(cat_content, width=12, md=10, class_name="mt-2 mt-md-2"),
    ], align="start", justify="center", class_name="h-100-scroll w-100 mx-auto")

    # define components
    navbar = cnavbar.layout(pathname, search, fluid=True)
    content = dbc.Container([content1, content2], fluid=True, class_name="h-100-scroll p-0")

    # return result
    return html.Div(children=[navbar, content], className="d-flex flex-column vh-100 overflow-scroll")


@app.callback(
    Output(f"id-{TAG}-collapse", "is_open"),
    Input(f"id-{TAG}-toggler", "n_clicks"),
    State(f"id-{TAG}-collapse", "is_open"),
)
def _toggle_catalog(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
