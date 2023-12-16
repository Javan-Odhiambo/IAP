from django.contrib import admin

from .models import CustomUser

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
