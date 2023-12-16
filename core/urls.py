from django.urls import path

from .views import (categoryPage, checkoutPage, homePage, productDetailPage,
                    searchResultsPage)

app_name = "core"

urlpatterns = [
    path("product/<slug:slug>/", productDetailPage, name="product-detail"),
    path("checkout/", checkoutPage, name="checkout"),
    path("search/<slug:slug>/", searchResultsPage, name="search-results"),
    path("category/<slug:slug>/", categoryPage, name="category"),
    path("", homePage, name="home"),
]
