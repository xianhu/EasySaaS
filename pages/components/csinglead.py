# _*_ coding: utf-8 _*_

"""
single accordion of page
"""

from dash import html


def layout(pathname, search, ad_id, ad_title, ad_class, ad_href, flush=False):
    """
    layout of component
    """
    button = html.Button(ad_title, className=f"accordion-button collapsed {ad_class}")
    return html.Div(children=[
        html.Div(html.H2(children=[
            html.A(button, href=ad_href, className="text-decoration-none"),
        ], className="accordion-header", style=None), className="accordion-item border-top-solid border-bottom-solid"),
    ], id=ad_id, className=f"accordion {'accordion-flush' if flush else ''}")
