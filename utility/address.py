# _*_ coding: utf-8 _*_

"""
html.A clicked automatically
"""

from dash import Input, Output, clientside_callback, html


class AddressAIO(html.A):
    """
    html.A clicked automatically
    """

    def __init__(self, aio_id, children=None, target=None):
        clientside_callback(
            """
            function(href) {
                element = document.getElementById("%s")
                if (element != null && href != null) {
                    element.click()
                }
                return href
            }
            """ % aio_id,
            Output(aio_id, "data-tmp"),
            Input(aio_id, "href"),
            prevent_initial_call=True,
        )
        return super().__init__(children, id=aio_id, target=target)
