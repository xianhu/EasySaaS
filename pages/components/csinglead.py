# _*_ coding: utf-8 _*_

"""
single accordion of page
"""

from dash import html


def layout(pathname, search, ad_id, ad_btcld, ad_btclass, flush=False):
    """
    layout of component
    """
    return html.Div(children=[
        html.Div(children=[
            html.H2(children=[
                html.Button(ad_btcld, className=f"accordion-button collapsed {ad_btclass}")
            ], className="accordion-header", style={"border-bottom": "thin solid rgba(0, 0, 0, 0.5)"}),
        ], className="accordion-item"),
    ], id=ad_id, className=f"accordion {'accordion-flush' if flush else ''}")
