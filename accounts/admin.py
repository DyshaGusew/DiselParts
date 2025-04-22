from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Buyer, Order, OrderItem


@admin.register(Buyer)
class BuyerAdmin(ModelAdmin):
    list_display = (
        "username",
        "email",
        "phone",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    search_fields = ("username", "email", "phone")
    list_filter = [
        "is_staff",
        "is_superuser",
    ]
    ordering = ("date_joined",)


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    fields = ('Product', 'quantity', 'get_price', 'get_total')
    readonly_fields = ('get_price', 'get_total')

    def get_price(self, obj):
        return obj.Product.sale_price

    get_price.short_description = 'Цена'

    def get_total(self, obj):
        return obj.quantity * obj.Product.sale_price

    get_total.short_description = 'Сумма'


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        "id",
        "User",
        "order_date",
        "total",
        "status",
    )
    list_display_links = ("User", "order_date", "total", "status")
    readonly_fields = ('total',)
    search_fields = ("User__username", "status")
    list_filter = [
        "status",
        "order_date",
    ]
    ordering = ("-order_date",)
    raw_id_fields = ("User",)

    inlines = (OrderItemInline,)
