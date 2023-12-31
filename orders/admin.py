from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from orders import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0


class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "order_status",
        "total_items",
        "total_amount",
        "order_date",
        "updated_at",
    ]
    list_filter = ["order_status", "order_date"]
    search_fields = ["id", "user__username", "user__email"]
    inlines = [OrderItemInline]

    def total_amount(self, obj):
        return obj.total_amount

    total_amount.short_description = "Total Amount"


class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at", "updated_at"]
    search_fields = ["id", "user__username", "user__email"]
    inlines = [CartItemInline]


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Cart, CartAdmin)
