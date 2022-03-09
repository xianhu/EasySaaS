# _*_ coding: utf-8 _*_

"""
single accordion of page
"""

from dash import html


def layout(pathname, search, ad_title, ad_href, flush=False):
    """
    layout of component
    """
    # define components
    _class1 = "text-primary" if ad_href == pathname else ""
    _class2 = "accordion-button collapsed bg-image-after-none bg-light"
    button = html.Button(ad_title, className=f"{_class1} {_class2}")
    button_a = html.A(button, href=ad_href, className="text-decoration-none")

    # return result
    return html.Div(children=[
        html.Div(children=[
            html.H2(button_a, className="accordion-header", style=None),
        ], className="accordion-item border-top-solid border-bottom-solid"),
    ], className=f"accordion {'accordion-flush' if flush else ''}")
