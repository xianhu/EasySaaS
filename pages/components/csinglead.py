# _*_ coding: utf-8 _*_

"""
single accordion of page
"""

from dash import html


def layout(pathname, search, ad_id, ad_title, ad_class, ad_href, flush=False):
    """
    layout of component
    """
    style = {"border-bottom": "thin solid rgba(0, 0, 0, 0.5)"}
    button = html.Button(ad_title, className=f"accordion-button collapsed {ad_class}")
    return html.Div(children=[
        html.Div(html.H2(children=[
            html.A(button, href=ad_href, className="text-decoration-none"),
        ], className="accordion-header", style=style), className="accordion-item"),
    ], id=ad_id, className=f"accordion {'accordion-flush' if flush else ''}")
