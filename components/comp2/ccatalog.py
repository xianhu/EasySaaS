# _*_ coding: utf-8 _*_

"""
catalog component
"""

from dash import html


def layout(catalog_list, class_name=None):
    """
    layout of component
    """
    # define components
    catalog_children = []
    for title_first, id_first, list_second in catalog_list:
        if isinstance(list_second, str):
            title, _id, href = title_first, id_first, list_second
            class_a = "text-decoration-none py-2 text-black hover-success"
            catalog_children.append(html.A(title, id=_id, href=href, className=class_a))
            continue

        # define components
        catalog_children.append(html.Div(title_first, className="small text-muted py-2"))
        for title, _id, href in list_second:
            class_a = "text-decoration-none py-2 text-black hover-success"
            catalog_children.append(html.A(title, id=_id, href=href, className=class_a))

    # return result
    return html.Div(catalog_children, className=f"d-flex flex-column px-4 {class_name}")
