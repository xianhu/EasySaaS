# _*_ coding: utf-8 _*_

"""
catalog of page
"""

from ..paths import PATH_USER

CATALOG_LIST = [
    ["ACCOUNT", None, [
        ("General", f"{PATH_USER}-general"),
        ("Security", f"{PATH_USER}-security"),
        ("Notifications", f"{PATH_USER}-notifications"),
    ]],
    ["BILLING", None, [
        ("Plan", f"{PATH_USER}-plan"),
        ("Payments", f"{PATH_USER}-payments"),
    ]],
]
