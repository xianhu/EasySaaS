# _*_ coding: utf-8 _*_

"""
adaptive layout
"""

import dash_bootstrap_components as dbc


def layout_many(col_children, align=None, justify="center", class_row="gx-0"):
    """
    adaptive layout with Row and Col
    :param col_children: [(col_item, col_widths, col_class), ...]
    """
    col_list = []
    for col_item, col_width, col_class in col_children:
        args_width = {"width": col_width[0], "md": col_width[1]}
        col_list.append(dbc.Col(col_item, **args_width, class_name=col_class))
    return dbc.Row(col_list, align=align, justify=justify, class_name=class_row)


def layout_two(item_left, width_left=(10, 3), item_right=None, width_right=None):
    """
    adaptive layout with Row and Col (min-vh-100)
    """
    if item_right is None:
        col_children = [(item_left, width_left, None)]
    else:
        class_left = "mt-auto mt-md-0"
        class_right = "mb-auto mb-md-0"
        width_right = width_right or (10, 3)
        col_children = [
            (item_left, width_left, class_left),
            (item_right, width_right, class_right),
        ]
    return layout_many(col_children, align="center", class_row="gx-0 min-vh-100")
