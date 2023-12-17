from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_status = models.CharField(
        max_length=50,
        choices=(
            ("pending", "Pending"),
            ("completed", "Completed"),
        ),
    )
    location = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_items(self):
        return self.order_items.count()

    @property
    def total_amount(self):
        total_amount = 0
        for item in self.order_items.all():
            total_amount += item.amount
        return total_amount

    class Meta:
        ordering = ["-id"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self) -> str:
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def amount(self):
        return self.product.price * self.quantity

    class Meta:
        ordering = ["-id"]
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        unique_together = ["order", "product"]

    def __str__(self) -> str:
        return f"Order #{self.order.id} - {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_items(self):
        return self.cart_items.count()

    @property
    def total_amount(self):
        total_amount = 0
        for item in self.cart_items.all():
            total_amount += item.amount
        return total_amount

    class Meta:
        ordering = ["-id"]
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self) -> str:
        return f"Cart #{self.id} for {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def amount(self):
        return self.product.price * self.quantity

    class Meta:
        ordering = ["-id"]
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ["cart", "product"]

    def __str__(self) -> str:
        return f"Cart #{self.cart.id} - {self.product.name}"
