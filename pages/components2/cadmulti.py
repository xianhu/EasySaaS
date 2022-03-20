# _*_ coding: utf-8 _*_

"""
accordion component
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(pathname, search, tag, catalog_list, flush=None, class_name=None):
    """
    layout of component
    """
    # define class
    class_seco0 = "text-decoration-none px-5 py-2 text-black hover-primary"
    class_seco1 = "text-decoration-none px-5 py-2 text-primary"

    # define components
    ad_item_list, active_id = [], None
    for index, (title_first, icon_first, list_second) in enumerate(catalog_list):
        item_id = f"id-{tag}-accordion-{index}"

        # define components
        address_list = []
        for title_second, href, *temp in list_second:
            if href == pathname:
                active_id = item_id
            _class = class_seco0 if href != pathname else class_seco1
            address_list.append(html.A(title_second, href=href, className=_class))

        # define components
        div = html.Div(address_list, className="d-flex flex-column py-2")
        ad_item_list.append(dbc.AccordionItem(div, item_id=item_id, title=title_first))

    # return result
    class_name = class_name or "border-top-solid border-bottom-solid"
    return dbc.Accordion(ad_item_list, active_item=active_id, flush=flush, class_name=class_name)
