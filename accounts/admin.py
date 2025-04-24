from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Buyer


@admin.register(Buyer)
class BuyerAdmin(ModelAdmin):
    list_display = (
        "email",
        "phone",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    search_fields = ("email", "phone")
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    ordering = ("date_joined",)
