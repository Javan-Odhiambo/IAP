"""
This module defines the URL patterns for the products app.
"""
from django.urls import path

from products import views

app_name = "products"

urlpatterns = [
    path("", view=views.product_list, name="product-list"),
    path(
        "<slug:slug>-<int:pk>/",
        view=views.product_detail,
        name="product-detail",
    ),
    path("search/", view=views.product_search, name="product-search"),
    path("categories/", view=views.categories, name="categories"),
]
