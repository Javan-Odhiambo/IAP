from orders.models import Cart, OrderItem
from products.models import Variant


def get_checkout_user_info(request):
    """Returns the checkout user info ie user, location and phone number"""
    user = request.user
    location = request.POST.get("location")
    phone_number = request.POST.get("phone_number")
    return user, location, phone_number


def create_order_items(cart, order):
    """Creates order items from cart items"""
    for item in cart.cart_items.all():
        # check if product variant is available and quantity is less than or equal to the available quantity
        if (
            not item.product_variant.is_available
            or item.quantity > item.product_variant.stock_quantity
        ):
            raise Exception(
                f"Product {item.product_variant.product.name} is not available"
            )
        # create order item
        OrderItem.objects.create(
            order=order,
            product_variant=item.product_variant,
            quantity=item.quantity,
        )
    # Delete cart items after creating order items
    cart.cart_items.all().delete()


def get_cart_info(request):
    """Returns the cart info from the request"""
    product_id = request.POST.get("product_id")
    size = request.POST.get("size")
    color = request.POST.get("color")
    quantity = int(request.POST.get("quantity", 1))
    return product_id, size, color, quantity


def get_product_variant(*args, **kwargs):
    """"""
    return Variant.objects.filter(**kwargs).first()


def get_user_cart(request):
    """Returns the cart for the current user"""
    return Cart.objects.filter(user=request.user).first()


def get_cart_item(cart, **kwargs):
    """Returns the cart item for the given cart and product variant"""
    return cart.cart_items.filter(**kwargs).first()
