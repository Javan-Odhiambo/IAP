from django.contrib import admin

from accounts.models import CustomUser, WishList, WishListItem

admin.site.register(CustomUser)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    ordering = (
        "email",
        "first_name",
        "last_name",
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class WishListItemInline(admin.TabularInline):
    model = WishListItem
    extra = 0


class WishListAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "updated_at"]
    list_filter = ["user", "created_at", "updated_at"]
    search_fields = ["id", "user__email", "item__name"]
    inlines = [WishListItemInline]


admin.site.register(WishList, WishListAdmin)
