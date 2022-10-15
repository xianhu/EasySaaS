# _*_ coding: utf-8 _*_

"""
accordion component
"""

from dash import html


def layout(title, _id, href, flush=None, class_name=None):
    """
    layout of component
    """
    # define components
    button = html.Button(title, id=_id, className="accordion-button collapsed")
    address = html.A(button, href=href, className="accordion-single text-decoration-none")

    # define components
    accordion_header = html.H2(address, className="accordion-header")
    accordion_item = html.Div(accordion_header, className=f"accordion-item {class_name}")

    # return result
    return html.Div(accordion_item, className=f"accordion {'accordion-flush' if flush else ''} accordion-catalog")
