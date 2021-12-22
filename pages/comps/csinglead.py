# _*_ coding: utf-8 _*_

"""
single accordion of page
"""

from dash import html


def layout(pathname, search, button_children, button_class, flush=False):
    """
    layout of components
    """
    # define components: style of header according to style-bs-accordion.css
    button = html.Button(button_children, className=f"accordion-button collapsed {button_class}")
    header = html.H2(button, className="accordion-header", style={"border-bottom": "thin solid rgba(0, 0, 0, 0.5)"})
    return html.Div(html.Div(header, className="accordion-item"), className=f"accordion {'accordion-flush' if flush else ''}")
