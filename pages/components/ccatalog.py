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
    c_first = "small text-muted mt-4 mb-2 px-4"
    c_second = "small text-decoration-none px-4 py-2"
    c_second0 = f"{c_second} text-black hover-primary"
    c_second1 = f"{c_second} text-white bg-primary"

    # define components
    catalog_item_list = []
    for title_first, icon_first, list_second in catalog_list:
        catalog_item_list.append(html.Div(title_first, className=c_first))

        # define components
        for title_second, href in list_second:
            _class = c_second0 if href != pathname else c_second1
            catalog_item_list.append(html.A(title_second, href=href, className=_class))

    # return result
    return html.Div(catalog_item_list, className=f"d-flex flex-column {class_name}")
