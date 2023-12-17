from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders import models
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from products.models import Product

# Create your views here.
@login_required
def checkout(request):
    """ Checkout view"""
    if request.method == 'POST':
        user = request.user
        loacation = request.POST.get('location')
        phone_number = request.POST.get('phone_number')
        cart = models.Cart.objects.filter(user=user).first()
        if cart is None or cart.cart_items.count() == 0:
            messages.error(request, "Cart is empty")
            return redirect('cart')  # Redirect to cart page
        # create order items from cart items
        order = models.Order.objects.create(user=user, order_status="pending", )
        for item in cart.cart_items.all():
            models.OrderItem.objects.create(
                order=order, product=item.product, quantity=item.quantity
            )
        cart.cart_items.all().delete()  # Delete cart items after creating order items
    return render(request, template_name='orders/checkout.html')

@login_required
def add_cart_item(request):
    """ Add a product to cart"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        # Get the cart for the current user
        cart, created = models.Cart.objects.get_or_create(user=request.user)
        # Create a new cart item with the product, or update the quantity if the item already exists
        cart_item, created = models.CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({"message": "Product added to cart"})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def remove_cart_item(request):
    """ Remove a product from cart"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        # Get the cart for the current user
        cart = models.Cart.objects.filter(user=request.user).first()
        if cart is not None:
            cart_item = models.CartItem.objects.filter(cart=cart, product=product).first()
            if cart_item is not None:
                cart_item.delete()
                return JsonResponse({"message": "Product removed from cart"})
        return JsonResponse({"error": "Invalid request"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)