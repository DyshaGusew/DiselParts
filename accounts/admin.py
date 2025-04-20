from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Buyer


@admin.register(Buyer)
class BuyerAdmin(ModelAdmin):
    list_display = ("username",)
