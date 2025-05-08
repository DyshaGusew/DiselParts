from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from ..models import Order, OrderItem


# Register your models here.
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
        "get_date",
        "total",
        "status",
    )
    list_display_links = ("id", "User", "get_date", "total", "status")
    readonly_fields = ('total', 'order_date')
    search_fields = ("User__username", "status")
    list_filter = [
        "status",
        "order_date",
    ]
    ordering = ("-order_date",)
    raw_id_fields = ("User",)
    inlines = (OrderItemInline,)

    fieldsets = (
        (None, {'fields': ('User', 'order_date', 'total', 'status', 'other_info')}),
        (
            'Рекомендации по статусам',
            {
                'classes': ('collapse',),
                'description': (
                    '<p><strong>Рекомендуемые статусы:</strong></p>'
                    '<ul>'
                    '<li><strong>Обрабатывается</strong>: Заказ принят и находится в процессе подготовки.</li>'
                    '<li><strong>Отправлен</strong>: Заказ передан в доставку.</li>'
                    '<li><strong>Доставлен</strong>: Заказ успешно доставлен клиенту.</li>'
                    '<li><strong>Отменен</strong>: Заказ отменен клиентом или администратором.</li>'
                    '</ul>'
                    '<p><strong>Другое:</strong> Нетривиальная сиутация, обязательно разъяснить в дополнительной информации</p>'
                ),
                'fields': (),
            },
        ),
    )

    # Настройка поля status
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['status'].help_text = (
            'Выберите статус из списка или введите свой. '
            'Рекомендуемые статусы описаны ниже.'
        )
        return form
