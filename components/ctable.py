# _*_ coding: utf-8 _*_

"""
table component
"""

import dash_bootstrap_components as dbc
from dash import html


def layout(
        tid, data, header_list, key_list, key_out=None, key_title=None,
        class_th=None, class_td=None, class_tr=None, class_data=None,
        bordered=True, borderless=True, hover=True, striped=True, class_name=None,
):
    """
    layout of component
    :param tid: table id
    :param data: data of table, list of dict
    :param header_list: header of table, list of str
    :param key_list: key of data, list of str
    :param key_out: key of data to be excluded, list of str
    :param key_title: key of data to be used as title, list of str
    :param class_th: class_name of th, a string
    :param class_td: class_name of td, a string
    :param class_tr: class_name of tr, a string
    :param class_data: class_name of data, list of dict
    :param bordered: bordered table
    :param borderless: borderless table
    :param hover: hover table
    :param striped: striped table
    :param class_name: class_name of table
    """
    # define class
    class_th = class_th or "text-center p-1"
    class_td = class_td or "text-center p-1"

    # define thead
    th_list = [html.Th(name, className=class_th) for name in header_list]
    thead = html.Thead(html.Tr(th_list, className=class_tr), id=f"{tid}-head")

    # define tr
    tr_list = []
    for index, item_info in enumerate(data or []):
        # define out's data and tr's title
        tr_index = item_info.get(key_out, index)
        tr_title = str(item_info.get(key_title, ""))

        # define class list
        class_info = class_data[index] if class_data else {}
        class_list = [class_info.get(key, "") for key in key_list]

        # define value list
        value_list = [item_info.get(key, "") for key in key_list]

        # define td_list
        class_list = [" ".join([class_td, _class]) for _class in class_list]
        td_list = [html.Td(v, className=c) for (v, c) in zip(value_list, class_list)]

        # define tr_list
        tr_id = {"type": f"{tid}-row", "index": tr_index}
        tr_list.append(html.Tr(td_list, id=tr_id, title=tr_title, className=class_tr))

    # return result
    kwargs = dict(bordered=bordered, borderless=borderless, hover=hover, striped=striped)
    return dbc.Table(children=[thead, html.Tbody(tr_list)], id=tid, **kwargs, class_name=class_name)
