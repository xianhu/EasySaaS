# _*_ coding: utf-8 _*_

"""
accordion component
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(catalog_list, ad_id, ad_active=None, flush=None, class_name=None):
    """
    layout of component
    """
    # define variables
    class_a = "text-white text-decoration-none px-5 py-3 accordion-background"

    # define components
    accordion_items = []
    for title_first, id_first, list_second in catalog_list:
        # define components
        address_list = [html.A(title, id=_id, href=href, className=class_a) for title, _id, href in list_second]

        # define components
        div = html.Div(address_list, className="d-flex flex-column")
        accordion_items.append(dbc.AccordionItem(div, title=title_first, item_id=id_first, class_name=class_name))

    # return result
    return dbc.Accordion(accordion_items, id=ad_id, active_item=ad_active, flush=flush, class_name="accordion-catalog")
