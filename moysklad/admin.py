from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import MoyskladProduct
from unfold.admin import ModelAdmin
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
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
from django.db.models import QuerySet


class DateModelForm(forms.ModelForm):
    image_url = forms.URLField(
        label="Ссылка на изображение",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "text-input",
                "data-input-class": "peer",
                "style": (
                    "background-color: transparent;"
                    "border: 1px solid #454545;"
                    "border-radius: 0.375rem;"
                    "padding: 0.5rem 0.75rem;"
                    "transition: border-color 0.2s;"
                ),
                "placeholder": "Введите URL изображения",
                "readonly": "readonly",  # Делаем поле только для чтения
            }
        ),
        help_text="Форматы: JPG, PNG, WebP",
    )

    class Meta:
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "readonly": "readonly"}),
        }


class LimitedMultipleChoicesDropdownFilter(MultipleChoicesDropdownFilter):
    def get_choices(self, changelist: QuerySet) -> list:
        choices = super().get_choices(changelist)
        return choices[:50]


@admin.register(MoyskladProduct)
class MoyskladProductAdmin(ModelAdmin):
    form = DateModelForm
    list_display = (
        "image_preview",
        "name",
        "article",
        "code",
        "price_value",
        "vat",
        "country_name",
        "supplier_legal_title",
        "is_active",
        "moysklad_url_link",
    )
    list_display_links = ("name", "code", "article", "image_preview")
    search_fields = ("name", "article", "code", "description")

    list_filter = [
        "vat_enabled",
        "archived",
        "price_type",
        "product_folder_name",
        'supplier_legal_title',
        "country_name",
        ("price_value", RangeNumericFilter),
    ]

    list_filter_submit = True
    list_filter_sheet = True
    list_fullwidth = False

    # Делаем все поля только для чтения
    readonly_fields = (
        "name",
        "moysklad_url",
        "description",
        "article",
        "code",
        "external_code",
        "price_value",
        "price_type",
        "min_price_value",
        "buy_price_value",
        "vat",
        "effective_vat",
        "vat_enabled",
        "effective_vat_enabled",
        "archived",
        "weight",
        "volume",
        "minimum_balance",
        "barcodes",
        "product_folder_name",
        "product_folder_description",
        "country_name",
        "supplier_legal_title",
        "supplier_actual_address",
        "supplier_phone",
        "images",
        "get_main_image_preview",
    )
    ordering = ("name", "price_value")
    filter_horizontal = ()

    fieldsets = (
        (
            None,
            {
                "fields": (),
                "description": format_html(
                    """
            <div style="
                padding: 16px;
                border-radius: 8px;
                margin-bottom: 20px;
                background-color: var(--background-muted);
                color: var(--foreground-muted);
                font-size: 14px;
                line-height: 1.6;
            ">
                <strong style="display: block; margin-bottom: 8px; color: var(--foreground-default);">
                    Внимание:
                </strong>
                Редактирование исходного товара доступно только в сервисе
                <a href="https://www.moysklad.ru/" target="_blank" style="color: var(--primary); font-weight: 500; text-decoration: underline;">
                    МойСклад</a>.<br>
                Для работы с товарами, доступными к продаже, перейдите в
                <a href="/admin/catalog/productforsale/" style="color: var(--primary); font-weight: 500; text-decoration: underline;">
                    раздел товаров для продажи
                </a>.
            </div>
            """
                ),
            },
        ),
        (
            "Основная информация",
            {
                "fields": (
                    ("name", "moysklad_url"),
                    "description",
                    ("article", "code", "external_code"),
                )
            },
        ),
        (
            "Цены",
            {
                "fields": (
                    "price_value",
                    "price_type",
                    "min_price_value",
                    "buy_price_value",
                )
            },
        ),
        (
            "Налоги и статус",
            {
                "fields": (
                    ("vat", "effective_vat"),
                    ("vat_enabled", "effective_vat_enabled", "archived"),
                )
            },
        ),
        (
            "Характеристики",
            {"fields": (("weight", "volume"), "minimum_balance", "barcodes")},
        ),
        (
            "Классификация",
            {
                "fields": (
                    "product_folder_name",
                    "product_folder_description",
                    "country_name",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Поставщик",
            {
                "fields": (
                    "supplier_legal_title",
                    "supplier_actual_address",
                    "supplier_phone",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Изображения", {"fields": ("images", "image_url", "get_main_image_preview")}),
    )

    def get_main_image_preview(self, obj):
        if not obj.images:
            return "Нет изображений"

        images_html = []
        for idx, img_data in enumerate(obj.images, start=1):
            img_url = img_data.get("medium") or img_data.get("original")
            if not img_url:
                continue

            images_html.append(
                format_html(
                    """
                    <div style="display: inline-block; margin-right: 15px; margin-bottom: 15px;">
                        <img src="{}" style="
                            max-height: 150px;
                            max-width: 200px;
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

    get_main_image_preview.short_description = "Все изображения товара"

    def image_preview(self, obj):
        if obj.images:
            img_url = obj.images[0].get("medium") or obj.images[0].get("thumbnail")
            if img_url:
                return format_html(
                    '<img src="{}" style="height: 50px; border-radius: 5px;"/>', img_url
                )
        return "-"

    image_preview.short_description = "Фото"

    def is_active(self, obj):
        return not obj.archived

    is_active.boolean = True
    is_active.short_description = "Активен"

    def clean_image_url(self):
        url = self.cleaned_data.get("image_url")
        if url and not url.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            raise ValidationError(
                "Неподдерживаемый формат изображения. Используйте JPG, PNG или WebP."
            )
        return url

    def moysklad_url_link(self, obj):
        if obj.moysklad_url:
            return format_html(
                '<a href="{}" target="_blank">Открыть в МойСклад</a>', obj.moysklad_url
            )
        return "-"

    moysklad_url_link.short_description = "Ссылка"

    def save_model(self, request, obj, form, change):
        # Переопределяем метод, чтобы предотвратить сохранение изменений
        pass

    def has_add_permission(self, request):
        # Запрещаем добавление новых записей
        return False

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление записей
        return False
