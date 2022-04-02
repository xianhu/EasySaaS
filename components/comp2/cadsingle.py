# _*_ coding: utf-8 _*_

"""
accordion component
"""

from dash import html


def layout(title, _id, path, curr_path=None, flush=None, class_name=None):
    """
    layout of component
    """
    # define class
    class_curr = "accordion-button collapsed bg-image-after-none text-primary"
    class_none = "accordion-button collapsed bg-image-after-none text-black hover-primary"

    # define components
    button = html.Button(title, className=class_curr if path == curr_path else class_none)
    address = html.A(button, id=_id, href=path, className="text-decoration-none")

    # define components
    header = html.H2(address, className="accordion-header")
    item = html.Div(header, className=f"accordion-item {class_name}")

    # return result
    return html.Div(item, className=f"accordion {'accordion-flush' if flush else ''}")
