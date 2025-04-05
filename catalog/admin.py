from django.contrib import admin
from .models import ProductForSale
from unfold.admin import ModelAdmin


@admin.register(ProductForSale)
class ProductForSaleAdmin(ModelAdmin):
    list_display = ["name", "sale_price", "is_active"]
