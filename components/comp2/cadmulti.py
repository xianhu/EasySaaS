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
    # define components
    accordion_items = []
    for title_first, id_first, list_second in catalog_list:
        address_list = []
        for title, _id, href in list_second:
            ctitle = html.Div(title, id=_id, className="text-white")
            address = html.A(ctitle, href=href, className="accordion-button text-decoration-none px-5 py-3")
            address_list.append(address)

        # define components
        div = html.Div(address_list, className="d-flex flex-column")
        accordion_items.append(dbc.AccordionItem(div, title=title_first, item_id=id_first))

    # return result
    class_name = class_name or "border-top-solid border-bottom-solid"
    return dbc.Accordion(accordion_items, id=ad_id, active_item=ad_active, flush=flush, class_name=class_name)
