# _*_ coding: utf-8 _*_

"""
accordion component
"""

from dash import html


def layout(title, _id, path, flush=None, class_name=None):
    """
    layout of component
    """
    # define class
    class_click = "accordion-button collapsed bg-image-after-none text-black hover-primary"

    # define components
    kwargs = dict(href=path, className="text-decoration-none")
    address = html.A(html.Button(title, id=_id, className=class_click), **kwargs)

    # define components
    header = html.H2(address, className="accordion-header")
    item = html.Div(header, className=f"accordion-item {class_name}")

    # return result
    return html.Div(item, className=f"accordion {'accordion-flush' if flush else ''}")
