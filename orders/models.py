from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import ExpressionWrapper, F, Sum, fields
from phonenumber_field.modelfields import PhoneNumberField

from products.models import Variant

User = get_user_model()


class Order(models.Model):
    """Model definition for Order."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_status = models.CharField(
        max_length=50,
        choices=(
            ("pending", "Pending"),
            ("completed", "Completed"),
        ),
        default="pending",
    )
    location = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_items(self):
        """Returns the total number of items in the order"""
        return sum([item.quantity for item in self.order_items.all()])

    @property
    def total_amount(self):
        """Returns the total amount of the order"""
        return sum([item.amount for item in self.order_items.all()])

    class Meta:
        ordering = ["-id"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self) -> str:
        """Returns the string representation of the order"""
        return f"Order #{self.id}"


class OrderItem(models.Model):
    """Model definition for OrderItem."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product_variant = models.ForeignKey("products.Variant", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    @property
    def amount(self):
        """Returns the amount of the order item"""
        return self.product_variant.product.price * self.quantity

    class Meta:
        ordering = ["-id"]
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        unique_together = ["order", "product_variant"]

    def __str__(self) -> str:
        """Returns the string representation of the order item"""
        return f"Order #{self.order.id} - {self.product_variant.product.name}"

    def clean(self, *args, **kwargs):
        """Validates the order item before saving"""
        # check if product variant is available and quantity is less than or equal to the available quantity
        product_variant = self.product_variant
        stock = product_variant.stock_quantity
        if (
            not product_variant
            or not product_variant.is_available
            or self.quantity > stock
        ):
            message = (
                f"Only {stock} products available"
                if stock > 0
                else "Product out of stock"
            )
            raise ValidationError(message)
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Saves the order item"""
        self.clean()
        # Update product variant quantity using F expressions
        expression = ExpressionWrapper(
            F("stock_quantity") - self.quantity,
            output_field=fields.PositiveIntegerField(),
        )
        Variant.objects.filter(pk=self.product_variant.pk).update(
            stock_quantity=expression
        )
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Model definition for Cart."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_items(self):
        """Returns the total number of items in the cart"""
        return self.cart_items.count()

    @property
    def total_amount(self):
        """Returns the total amount of the cart"""
        return self.cart_items.aggregate(Sum("amount"))["amount__sum"] or 0

    class Meta:
        ordering = ["-id"]
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self) -> str:
        """Returns the string representation of the cart"""
        return f"Cart #{self.id} for {self.user.email}"


class CartItem(models.Model):
    """Model definition for CartItem."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product_variant = models.ForeignKey("products.Variant", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    @property
    def amount(self):
        """Returns the amount of the cart item"""
        return self.product.price * self.quantity

    class Meta:
        ordering = ["-id"]
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ["cart", "product_variant"]

    def __str__(self) -> str:
        """Returns the string representation of the cart item"""
        return f"Cart #{self.cart.id} - {self.product.name}"

    def clean(self, *args, **kwargs):
        """Validates the cart item before saving"""
        # check if product variant is available and quantity is less than or equal to the available quantity
        if (
            not self.product_variant.is_available
            or self.quantity > self.product_variant.stock_quantity
        ):
            raise ValidationError("Product is not available")
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Saves the cart item"""
        self.clean()
        super().save(*args, **kwargs)
