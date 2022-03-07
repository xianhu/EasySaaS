# _*_ coding: utf-8 _*_

"""
single accordion of page
"""

from dash import html


def layout(pathname, search, ad_id, ad_title, ad_class, ad_href, flush=False):
    """
    layout of component
    """
    _class = "accordion-button collapsed bg-image-after-none"
    button = html.Button(ad_title, className=f"{_class} {ad_class}")
    button_a = html.A(button, href=ad_href, className="text-decoration-none")
    return html.Div(children=[
        html.Div(children=[
            html.H2(button_a, className="accordion-header", style=None),
        ], className="accordion-item border-top-solid border-bottom-solid"),
    ], id=ad_id, className=f"accordion {'accordion-flush' if flush else ''}")
