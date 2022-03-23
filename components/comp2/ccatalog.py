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
    class_first = "small text-muted mt-4 mb-2 px-4"
    class_seco0 = "small text-decoration-none px-4 py-2 text-black hover-primary"
    class_seco1 = "small text-decoration-none px-4 py-2 text-white bg-primary"

    # define components
    catalog_item_list = []
    for title_first, icon_first, list_second in catalog_list:
        catalog_item_list.append(html.Div(title_first, className=class_first))

        # define components
        for title_second, href, *temp in list_second:
            _class = class_seco0 if href != pathname else class_seco1
            catalog_item_list.append(html.A(title_second, href=href, className=_class))

    # return result
    return html.Div(catalog_item_list, className=f"d-flex flex-column {class_name}")
