from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from ..models import Order, OrderItem
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect


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
    actions = [
        'apply_status',
    ]

    # Настройка поля status
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['status'].help_text = (
            'Выберите статус из списка или введите свой. '
            'Рекомендуемые статусы описаны ниже.'
        )
        return form

    @admin.action(description="Изменить статус заказов")
    def apply_status(self, request, queryset):
        if 'apply' in request.POST:
            try:
                selected_ids = request.POST.getlist('_selected_action')
                queryset = self.get_queryset(request).filter(pk__in=selected_ids)

                new_status = request.POST.get('status', '')
                other_info = request.POST.get('other_info', '')

                if not new_status:
                    raise ValueError("Не выбран статус")

                updated = 0
                for order in queryset:
                    order.status = new_status
                    if other_info:
                        order.other_info = other_info
                    order.save()
                    updated += 1

                self.message_user(
                    request,
                    f"Статус '{new_status}' и дополнительная информация применены к {updated} заказам",
                    messages.SUCCESS,
                )
                return HttpResponseRedirect(request.get_full_path())
            except Exception as e:
                self.message_user(
                    request,
                    f"Ошибка: {str(e)}",
                    messages.ERROR,
                )
                return HttpResponseRedirect(request.get_full_path())

        return render(
            request,
            'order/apply_status_intermediate.html',
            context={
                'title': "Изменение статуса заказов",
                'orders': queryset,
                'opts': self.model._meta,
                'action': 'apply_status',
                'back_url': request.get_full_path(),
                'selected_ids': request.POST.getlist('_selected_action'),
            },
        )
