# _*_ coding: utf-8 _*_

"""
single accordion of page
"""

from dash import html


def layout(pathname, search, button_children, button_class, header_style, flush=False):
    """
    layout of components
    """
    button = html.Button(button_children, className=f"accordion-button collapsed {button_class}")
    header = html.H2(button, className="accordion-header", style=header_style)
    item = html.Div(header, className="accordion-item")
    return html.Div(item, className=f"accordion {'accordion-flush' if flush else ''}")
