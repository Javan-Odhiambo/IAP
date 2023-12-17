from django.contrib import admin

from products import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image")


class VariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "variant_unit",
        "stock_quantity",
        "is_available",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_available", "created_at", "updated_at")


class VariantUnitAdmin(admin.ModelAdmin):
    list_display = ("size", "color")


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ("value",)


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ("value",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductImage, ProductImageAdmin)
admin.site.register(models.Variant, VariantAdmin)
admin.site.register(models.VariantUnit, VariantUnitAdmin)
admin.site.register(models.ProductSize, ProductSizeAdmin)
admin.site.register(models.ProductColor, ProductColorAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Review, ReviewAdmin)
