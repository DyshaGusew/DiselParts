from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from ..models import Basket, BasketItem


class BasketItemInline(TabularInline):
    model = BasketItem
    extra = 0
    fields = ('Product', 'quantity', 'get_price', 'get_total')
    readonly_fields = ('get_price', 'get_total')

    def get_price(self, obj):
        return obj.Product.sale_price

    get_price.short_description = 'Цена'

    def get_total(self, obj):
        return obj.quantity * obj.Product.sale_price

    get_total.short_description = 'Сумма'


@admin.register(Basket)
class BasketAdmin(ModelAdmin):
    list_display = (
        "id",
        "User",
        "products_count",
        "total",
    )
    list_display_links = ("id", "User", "products_count", "total")
    readonly_fields = (
        'total',
        'products_count',
    )
    search_fields = ("User__username",)
    raw_id_fields = ("User",)

    inlines = (BasketItemInline,)
