# _*_ coding: utf-8 _*_

"""
accordion component
"""

from dash import html


def layout(title, _id, path, flush=None, class_name=None):
    """
    layout of component
    """
    # define components
    ctitle = html.Div(title, id=_id, className="text-black hover-primary")
    button = html.Button(ctitle, className="accordion-button collapsed bg-image-after-none")
    address = html.A(button, href=path, className="text-decoration-none")

    # define components
    header = html.H2(address, className="accordion-header")
    item = html.Div(header, className=f"accordion-item {class_name}")

    # return result
    return html.Div(item, className=f"accordion {'accordion-flush' if flush else ''}")
