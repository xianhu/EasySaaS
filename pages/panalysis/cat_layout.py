# _*_ coding: utf-8 _*_

"""
catalog layout of page
"""

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

from app import app

from ..paths import *
from .cat_config import CATALOG_LIST

TAG = "analysis"


def layout(pathname, search):
    """
    layout of catalog
    """
    # define components
    accord_item_list = []
    for title, info in CATALOG_LIST:
        item_title = html.Div(children=[
            html.I(className=info["icon"]),
            html.Div(title),
        ], className="d-flex")

        item_children = []
        for title_2, path in info["items"]:
            item_children.append(html.A(title_2, href=path))

        accord_item_list.append(dbc.AccordionItem(children=item_children, title=title))

    return [dbc.Accordion(accord_item_list, flush=True),]
