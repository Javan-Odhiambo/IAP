from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("add_cart_item/", views.add_cart_item, name="add_cart_item"),
    path("remove_cart_item/", views.remove_cart_item, name="remove_cart_item"),
]
