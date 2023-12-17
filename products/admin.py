from django.contrib import admin

from products import models


class ProductInline(admin.TabularInline):
    """Tabular Inline View for Product"""

    model = models.Product
    fields = ("name", "price", "category", "description")
    extra = 0

    def has_add_permission(self, request, obj=None):
        """Return False to hide the add button"""
        return False

    def has_change_permission(self, request, obj=None):
        """Return False to hide the change button"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Return False to hide the delete button"""
        return False


class ReviewInline(admin.TabularInline):
    """Tabular Inline View for Review"""

    model = models.Review
    extra = 0


class ProductImageInline(admin.TabularInline):
    """Tabular Inline View for ProductImage"""

    model = models.ProductImage
    extra = 0


class VariantInline(admin.TabularInline):
    """Tabular Inline View for Variant"""

    model = models.Variant
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    """Admin View for Product"""

    fields = (
        "name",
        "slug",
        "description",
        "price",
        "category",
    )
    list_display = ("name", "price", "category", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, VariantInline, ReviewInline]


class ProductSizeAdmin(admin.ModelAdmin):
    """Admin View for ProductSize"""

    list_display = ("value",)

    def has_module_permission(self, request):
        """Return False to hide the model admin from index page"""
        return False


class ProductColorAdmin(admin.ModelAdmin):
    """Admin View for ProductColor"""

    list_display = ("value",)

    def has_module_permission(self, request):
        """Return False to hide the model admin from index page"""
        return False


class CategoryAdmin(admin.ModelAdmin):
    """Admin View for Category"""

    list_display = ("name", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductInline]


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductSize, ProductSizeAdmin)
admin.site.register(models.ProductColor, ProductColorAdmin)
admin.site.register(models.Category, CategoryAdmin)
