# _*_ coding: utf-8 _*_

"""
catalog component
"""

from dash import html


def layout(pathname, search, catalog_list, class_name=None):
    """
    layout of component
    """
    # define class
    class_title = "small text-muted px-4 py-2"
    class_none = "small text-decoration-none px-4 py-2 text-black hover-primary"
    class_curr = "small text-decoration-none px-4 py-2 text-white bg-primary"

    # define components
    catalog_item_list = []
    for title_first, id_first, list_second in catalog_list:
        if isinstance(list_second, str):
            _class = class_curr if list_second == pathname else class_none
            catalog_item_list.append(html.A(title_first, id=id_first, href=list_second, className=_class))
        else:
            catalog_item_list.append(html.Div(title_first, className=class_title))
            for title, _id, href in list_second:
                _class = class_curr if href == pathname else class_none
                catalog_item_list.append(html.A(title, id=_id, href=href, className=_class))

    # return result
    return html.Div(catalog_item_list, className=f"d-flex flex-column {class_name}")
