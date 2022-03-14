# _*_ coding: utf-8 _*_

"""
single accordion component
"""

from dash import html


def layout(pathname, search, ad_title, ad_href, flush=None, class_item=None):
    """
    layout of component
    """
    # define components
    _class0 = "text-primary" if ad_href == pathname else ""
    _class1 = "accordion-button collapsed bg-image-after-none"
    button = html.Button(ad_title, className=f"{_class0} {_class1}")
    button_a = html.A(button, href=ad_href, className="text-decoration-none")

    # return result
    return html.Div(children=[
        html.Div(children=[
            html.H2(button_a, className="accordion-header"),
        ], className=f"accordion-item {class_item or 'bg-light'}"),
    ], className=f"accordion {'accordion-flush' if flush else ''}")
