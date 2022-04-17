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
            ctitle = html.Div(title_first, id=id_first, className="text-black hover-primary")
            address = html.A(ctitle, href=list_second, className="text-decoration-none px-4 py-2")
            catalog_children.append(address)
            continue

        # define components
        catalog_children.append(html.Div(title_first, className="small text-muted px-4 py-2"))
        for title, _id, href in list_second:
            ctitle = html.Div(title, id=_id, className="text-black hover-primary")
            address = html.A(ctitle, href=href, className="text-decoration-none px-4 py-2")
            catalog_children.append(address)

    # return result
    return html.Div(catalog_children, className=f"d-flex flex-column {class_name}")
