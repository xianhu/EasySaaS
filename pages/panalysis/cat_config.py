# _*_ coding: utf-8 _*_

"""
catalog config of page
"""

from ..paths import PATH_ANALYSIS


CATALOG_LIST = [
    ["Dashboards", {"icon": "bi bi-house-door", "items": [
        ("Analytics", f"{PATH_ANALYSIS}-db-analytics"),
        ("CustomRM", f"{PATH_ANALYSIS}-db-cumtomrm"),
        ("Ecommerce", f"{PATH_ANALYSIS}-db-ecommerce"),
        ("Projects", f"{PATH_ANALYSIS}-db-projects"),
    ]}],
    ["Ecommerce", {"icon": "bi bi-coin", "items": [
        ("Products", f"{PATH_ANALYSIS}-ec-products"),
        ("Products Details", f"{PATH_ANALYSIS}-ec-prodetails"),
        ("Order", f"{PATH_ANALYSIS}-ec-order"),
        ("Order Details", f"{PATH_ANALYSIS}-ec-orddetails"),
        ("Customers", f"{PATH_ANALYSIS}-ec-customers"),
        ("Shopping Cart", f"{PATH_ANALYSIS}-ec-shopcart"),
        ("Checkout", f"{PATH_ANALYSIS}-ec-checkout"),
        ("Sellers", f"{PATH_ANALYSIS}-ec-sellers"),
    ]}],
    ["Email", {"icon": "bi bi-envelope", "items": [
        ("Inbox", f"{PATH_ANALYSIS}-em-inbox"),
        ("Read Email", f"{PATH_ANALYSIS}-em-read"),
    ]}],
    ["Project", {"icon": "bi bi-cast", "items": [
        ("List", f"{PATH_ANALYSIS}-pj-list"),
        ("Details", f"{PATH_ANALYSIS}-pj-details"),
        ("Gantt", f"{PATH_ANALYSIS}-pj-gantt"),
        ("Create Project", f"{PATH_ANALYSIS}-pj-create"),
    ]}],
    ["Tasks", {"icon": "bi bi-list-task", "items": [
        ("List", f"{PATH_ANALYSIS}-ts-list"),
        ("Details", f"{PATH_ANALYSIS}-ts-details"),
        ("Kanban Board", f"{PATH_ANALYSIS}-ts-board"),
    ]}],
    ["Pages", {"icon": "bi bi-file-break", "items": [
        ("Profile", f"{PATH_ANALYSIS}-pg-profile"),
        ("Invoice", f"{PATH_ANALYSIS}-pg-invoice"),
        ("Pricing", f"{PATH_ANALYSIS}-pg-pricing"),
        ("Maintenance", f"{PATH_ANALYSIS}-pg-maintenance"),
        ("Starter Page", f"{PATH_ANALYSIS}-pg-starter"),
        ("With Preloader", f"{PATH_ANALYSIS}-pg-preloader"),
        ("Timeline", f"{PATH_ANALYSIS}-pg-timeline"),
    ]}],
    ["Layouts", {"icon": "bi bi-columns-gap", "items": [
        ("Horizontal", f"{PATH_ANALYSIS}-ly-horizontal"),
        ("Detached", f"{PATH_ANALYSIS}-ly-detached"),
    ]}],
]
