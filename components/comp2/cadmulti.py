# _*_ coding: utf-8 _*_

"""
accordion component
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(catalog_list,  flush=None, class_name=None):
    """
    layout of component
    """
    # define class
    class_click = "text-decoration-none px-5 py-2 text-black hover-primary"

    # define components
    accordion_item_list = []
    for title_first, id_first, list_second in catalog_list:
        address_list = []
        for title, _id, path in list_second:
            kwargs = dict(id=_id, href=path, className=class_click)
            address_list.append(html.A(title, **kwargs))

        # define components
        div = html.Div(address_list, className="d-flex flex-column py-2")
        accordion_item_list.append(dbc.AccordionItem(div, title=title_first, item_id=id_first))

    # return result
    class_name = class_name or "border-top-solid border-bottom-solid"
    return dbc.Accordion(accordion_item_list, active_item=None, flush=flush, class_name=class_name)
