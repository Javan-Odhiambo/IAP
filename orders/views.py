from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from orders import models
from orders.services import (
    create_order_items,
    get_cart_info,
    get_cart_item,
    get_checkout_user_info,
    get_product_variant,
    get_user_cart,
)
from products.models import Product, ProductColor, ProductSize, Variant


# Create your views here.
@login_required
def checkout(request):
    """Checkout view"""
    if request.method == "POST":
        # Get the current user, location and phone number from the request
        user, location, phone_number = get_checkout_user_info(request)
        # Get the cart for the current user
        cart = get_object_or_404(models.Cart, user=user)
        # Check if the cart is empty
        if cart.cart_items.count() == 0:
            messages.error(request, "Cart is empty")
            return redirect("core:home")
        try:
            with transaction.atomic():
                # create order items from cart items
                order = models.Order.objects.create(
                    user=user,
                    order_status="pending",
                    location=location,
                    phone_number=phone_number,
                )
                create_order_items(cart, order)
        except Exception as e:
            messages.error(request, "An error occurred while processing your order")
            return redirect("orders:checkout")
    return render(request, template_name="orders/checkout.html", context={"cart": cart})


@login_required
def add_cart_item(request):
    """Add a product to cart"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    # Get the product_id, size, color and quantity from the request
    product_id, size, color, quantity = get_cart_info(request)
    # Get the product, size and color
    product = get_object_or_404(Product, id=product_id)
    product_size = get_object_or_404(ProductSize, size=size)
    product_color = get_object_or_404(ProductColor, color=color)
    # Get the product variant
    product_variant = get_product_variant(
        product=product, size=product_size, color=product_color
    )
    if not product_variant:
        return JsonResponse({"error": "Invalid request"}, status=400)
    # Get the cart for the current user
    cart, created = models.Cart.objects.get_or_create(
        user=request.user, product_variant=product_variant
    )
    # Create a new cart item with the product, or update the quantity if the item already exists
    cart_item, created = models.CartItem.objects.update_or_create(
        cart=cart,
        product_variant=product_variant,
        defaults={"quantity": models.F("quantity") + quantity},
    )
    return JsonResponse({"message": "Product added to cart"}, status=200)


@login_required
def remove_cart_item(request):
    """Remove a product from cart"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    # Get the product_id, size, color, quanity from the request
    product_id, size, color, quantity = get_cart_info(request)
    # Get the product, size and color
    product = get_object_or_404(Product, id=product_id)
    product_size = get_object_or_404(ProductSize, size=size)
    product_color = get_object_or_404(ProductColor, color=color)
    # Get the product variant
    product_variant = get_product_variant(
        product=product, size=product_size, color=product_color
    )
    if not product_variant:
        return JsonResponse({"error": "Invalid request"}, status=400)
    # Get the cart for the current user and the cart item
    cart = get_user_cart(user=request.user)
    cart_item = get_cart_item(cart=cart, product_variant=product_variant)
    if not cart or not cart_item:
        return JsonResponse({"error": "Invalid request"}, status=400)
    if quantity < 1:
        return JsonResponse({"error": "Invalid request"}, status=400)
    if cart_item.quantity > quantity:
        cart_item.quantity -= quantity
        cart_item.save()
        return JsonResponse({"message": "Product quantity updated"}, status=200)
    if cart_item.quantity == quantity:
        cart_item.delete()
    return JsonResponse({"message": "Product removed from cart"}, status=200)
