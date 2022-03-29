# _*_ coding: utf-8 _*_

"""
accordion component
"""

from dash import html


def layout(pathname, search, title, _id, href, flush=None, class_name=None):
    """
    layout of component
    """
    # define class
    class_none = "accordion-button collapsed bg-image-after-none text-black hover-primary"
    class_curr = "accordion-button collapsed bg-image-after-none text-primary"

    # define components
    button = html.Button(title, className=class_curr if href == pathname else class_none)
    address = html.A(button, id=_id, href=href, className="text-decoration-none")

    # define components
    header = html.H2(address, className="accordion-header")
    item = html.Div(header, className=f"accordion-item {class_name}")

    # return result
    return html.Div(item, className=f"accordion {'accordion-flush' if flush else ''}")
