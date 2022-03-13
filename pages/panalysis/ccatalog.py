# _*_ coding: utf-8 _*_

"""
catalog component
"""

import dash_bootstrap_components as dbc
from dash import html

from . import cupload
from ..components import csinglead
from ..paths import PATH_ANALYSIS

TAG = "analysis-catalog"
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


def layout(pathname, search, class_name=None):
    """
    layout of component
    """
    # define components
    upload = cupload.layout(pathname, search, class_name="my-4")

    # define components
    _class, ad_href = "border-top-solid bg-light", f"{PATH_ANALYSIS}-table"
    table = csinglead.layout(pathname, search, "Table", ad_href, flush=True, class_item=_class)

    # define components
    ad_item_list, active_id = [], None
    class_second = "text-decoration-none px-5 py-2"
    for index, (title_first, icon_first, list_second) in enumerate(CATALOG_LIST):
        item_id = f"id-{TAG}-accordion-{index}"

        # define components
        ad_children = []
        for title_second, path in list_second:
            if path == pathname:
                active_id = item_id

            # define components
            _class = "text-black hover-primary" if path != pathname else "text-primary"
            ad_children.append(html.A(title_second, href=path, className=f"{class_second} {_class}"))
        ad_item_list.append(dbc.AccordionItem(ad_children, item_id=item_id, title=title_first))

    # define components
    _class, _id = "border-top-solid border-bottom-solid", f"id-{TAG}-accordion"
    accordion = dbc.Accordion(ad_item_list, id=_id, active_item=active_id, flush=True, class_name=_class)

    # return result
    return html.Div([upload, table, accordion], className=class_name)
