# _*_ coding: utf-8 _*_

"""
catalog component
"""

from dash import html


def layout(catalog_list, class_name=None):
    """
    layout of component
    """
    # define class
    class_title = "small text-muted px-4 py-2"
    class_click = "text-decoration-none px-4 py-2 text-black hover-primary"

    # define components
    catalog_item_list = []
    for title_first, id_first, list_second in catalog_list:
        if isinstance(list_second, str):
            kwargs = dict(id=id_first, href=list_second, className=class_click)
            catalog_item_list.append(html.A(title_first, **kwargs))
            continue

        # define components
        catalog_item_list.append(html.Div(title_first, className=class_title))
        for title, _id, path in list_second:
            kwargs = dict(id=_id, href=path, className=class_click)
            catalog_item_list.append(html.A(title, **kwargs))

    # return result
    return html.Div(catalog_item_list, className=f"d-flex flex-column {class_name}")
