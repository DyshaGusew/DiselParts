from decimal import Decimal
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from regex import P
from .models import ProductForSale
from unfold.admin import ModelAdmin
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from unfold.contrib.filters.admin import (
    FieldTextFilter,
    ChoicesDropdownFilter,
    MultipleChoicesDropdownFilter,
    MultipleRelatedDropdownFilter,
    RangeDateFilter,
    RangeDateTimeFilter,
    RangeNumericFilter,
    RelatedDropdownFilter,
    SingleNumericFilter,
    TextFilter,
)


class ProductForSaleForm(forms.ModelForm):
    class Meta:
        model = ProductForSale
        fields = '__all__'


@admin.register(ProductForSale)
class ProductForSaleAdmin(ModelAdmin):
    form = ProductForSaleForm
    list_display = (
        'image_preview',
        'name',
        'article',
        'price_info',
        'markup_percent',
        'supplier_legal_title',
        'country',
        'is_active',
    )
    list_display_links = ('image_preview', 'name', 'article')
    search_fields = ('name', 'article', 'moysklad_product__code')
    list_filter = [
        'is_active',
        'group',
        'country',
        'supplier_legal_title',
        ('sale_price', RangeNumericFilter),
        ('markup_percent', RangeNumericFilter),
    ]

    list_filter_submit = True
    list_filter_sheet = True
    list_fullwidth = False

    readonly_fields = (
        'get_images_preview',
        'get_moysklad_link',
        'calculated_price_info',
    )
    ordering = ('name',)
    list_select_related = ('moysklad_product',)

    fieldsets = (
        (
            'Основная информация',
            {
                'fields': (
                    'moysklad_product',
                    'get_moysklad_link',
                    'name',
                    'article',
                    'description',
                    'is_active',
                )
            },
        ),
        (
            'Ценообразование',
            {
                'fields': (
                    'sale_price_moy_sklad',
                    'markup_percent',
                    'calculated_price_info',
                    'sale_price',
                )
            },
        ),
        (
            'Классификация',
            {
                'fields': (
                    'group',
                    'country',
                    'supplier_legal_title',
                ),
                'classes': ('collapse',),
            },
        ),
        (
            'Дополнительно',
            {
                'fields': (
                    'views',
                    'rating',
                ),
                'classes': ('collapse',),
            },
        ),
        (
            'Изображения',
            {
                'fields': ('get_images_preview',),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('moysklad_product')

    def image_preview(self, obj):
        if obj.moysklad_product and obj.moysklad_product.images:
            img_url = obj.moysklad_product.images[0].get(
                'medium'
            ) or obj.moysklad_product.images[0].get('thumbnail')
            if img_url:
                return format_html(
                    '<img src="{}" style="height: 50px; border-radius: 5px;"/>', img_url
                )
        return "-"

    image_preview.short_description = "Фото"

    def get_images_preview(self, obj):
        if not obj.moysklad_product or not obj.moysklad_product.images:
            return "Нет изображений"

        images_html = []
        for idx, img_data in enumerate(obj.moysklad_product.images, start=1):
            img_url = img_data.get('medium') or img_data.get('original')
            if not img_url:
                continue

            images_html.append(
                format_html(
                    """
                    <div style="display: inline-block; margin-right: 15px; margin-bottom: 15px;">
                        <img src="{}" style="
                            max-height: 200px;
                            max-width: 250px;
                            border-radius: 8px;
                            box-shadow: 1px 1px 6px rgba(0,0,0,0.2);
                            object-fit: contain;
                        "/>
                        <div style="text-align: center; margin-top: 5px; font-size: 12px;">
                            Изображение {}
                        </div>
                    </div>
                    """,
                    img_url,
                    idx,
                )
            )

        return (
            format_html(
                '<div style="display: flex; flex-wrap: wrap;">{}</div>',
                mark_safe("".join(images_html)),
            )
            if images_html
            else "Нет корректных изображений"
        )

    get_images_preview.short_description = "Все изображения товара"

    def price_info(self, obj):
        base_price = obj.sale_price_moy_sklad
        sale_price = obj.sale_price

        if base_price == sale_price:
            return format_html(
                '<div style="font-weight: 500;">{} ₽</div>', format(base_price, '.2f')
            )

        return format_html(
            '<div>'
            '<div style="text-decoration: line-through; color: #999; font-size: 0.9em;">{} ₽</div>'
            '<div style="font-weight: 500; color: #d32f2f;">{} ₽</div>'
            '</div>',
            format(base_price, '.2f'),
            format(sale_price, '.2f'),
        )

    price_info.short_description = "Цена"
    price_info.admin_order_field = 'sale_price'

    def markup_info(self, obj):
        if obj.markup_percent == 0.00:
            return "-"

    markup_info.short_description = "Наценка"
    markup_info.admin_order_field = 'markup_percent'

    def calculated_price_info(self, obj):
        if obj.markup_percent == 0.00:
            return "Наценка не применена"

        calculated = obj.sale_price_moy_sklad * (1 + obj.markup_percent / 100)
        return format_html(
            '<div style="margin-top: 10px;">'
            '<div>Расчетная цена: <strong>{} ₽</strong></div>'
            '<div style="font-size: 0.9em; color: #666;">Базовая цена {} ₽ × (1 + {}%)</div>'
            '</div>',
            format(calculated, '.2f'),
            format(obj.sale_price_moy_sklad, '.2f'),
            format(obj.markup_percent, '.2f'),
        )

    calculated_price_info.short_description = "Информация о расчете цены"

    def get_moysklad_link(self, obj):
        if not obj.moysklad_product or not obj.moysklad_product.id:
            return "–"  # Use en dash for better typography

        moysklad_url = obj.moysklad_product.moysklad_url

        return format_html(
            '<a href="{}" target="_blank" style="display: inline-flex; align-items: center; padding: 6px 12px; background-color: #f0f4f8; color: #1a73e8; text-decoration: none; border-radius: 4px; font-size: 14px; font-weight: 500;">'
            '<svg style="width: 16px; height: 16px; margin-right: 6px; fill: currentColor;" viewBox="0 0 24 24">'
            '<path d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z" />'
            '</svg>'
            '<span>Открыть в МойСклад</span>'
            '</a>',
            moysklad_url,
        )

    get_moysklad_link.short_description = "Ссылка на МойСклад"
    get_moysklad_link.allow_tags = True

    def save_model(self, request, obj, form, change):
        # Автоматический пересчет цены при изменении наценки
        if (
            'markup_percent' in form.changed_data
            or 'sale_price_moy_sklad' in form.changed_data
        ):
            obj.sale_price = obj.sale_price_moy_sklad * (1 + obj.markup_percent / 100)

        super().save_model(request, obj, form, change)

    actions = ['apply_markup', 'activate_selected', 'deactivate_selected']

    @admin.action(description="Активировать выбранные товары")
    def activate_selected(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} товаров активировано", messages.SUCCESS)

    @admin.action(description="Деактивировать выбранные товары")
    def deactivate_selected(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request, f"{updated} товаров деактивировано", messages.SUCCESS
        )

    @admin.action(description="Применить наценку к выбранным товарам")
    def apply_markup(self, request, queryset):
        if 'apply' in request.POST:
            try:
                # Получаем выбранные товары из POST-данных
                selected_ids = request.POST.getlist('_selected_action')
                queryset = self.get_queryset(request).filter(pk__in=selected_ids)

                markup = float(request.POST.get('markup', 0))
                updated = 0
                for product in queryset:
                    product.markup_percent = markup
                    product.sale_price = product.sale_price_moy_sklad * Decimal(
                        1.0 + markup / 100.0
                    )
                    product.save()
                    updated += 1

                self.message_user(
                    request,
                    f"Наценка {markup}% применена к {updated} товарам",
                    messages.SUCCESS,
                )
                return HttpResponseRedirect(request.get_full_path())
            except ValueError:
                self.message_user(
                    request,
                    "Ошибка: введите корректное число для наценки",
                    messages.ERROR,
                )
                return HttpResponseRedirect(request.get_full_path())

        # Показываем промежуточную страницу
        return render(
            request,
            'catalog/apply_markup_intermediate.html',
            context={
                'title': "Применить наценку",
                'products': queryset,
                'opts': self.model._meta,
                'action': 'apply_markup',
                'back_url': request.get_full_path(),
                # Добавляем скрытые поля с выбранными объектами
                'selected_ids': request.POST.getlist('_selected_action'),
            },
        )
