# _*_ coding: utf-8 _*_

"""
single accordion component
"""

from dash import html


def layout(pathname, search, ad_title, ad_href, flush=None, class_0=None, class_1=None):
    """
    layout of component
    """
    # define class
    class_0 = class_0 or "bg-light"
    class_1 = class_1 or "bg-light text-primary"

    # define components
    _class0 = class_0 if ad_href != pathname else class_1
    _class1 = "accordion-button collapsed bg-image-after-none"
    button = html.Button(ad_title, className=f"{_class0} {_class1}")
    button_a = html.A(button, href=ad_href, className="text-decoration-none")

    # return result
    return html.Div(children=[
        html.Div(children=[
            html.H2(button_a, className="accordion-header", style=None),
        ], className="accordion-item border-top-solid border-bottom-solid"),
    ], className=f"accordion {'accordion-flush' if flush else ''}")
