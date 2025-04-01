from django.contrib import admin
from moysklad.models import MoyskladProduct
from django import forms
from unfold.admin import ModelAdmin


class DateModelForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }


@admin.register(MoyskladProduct)
class MoyskladProductAdmin(ModelAdmin):
    form = DateModelForm
    list_display = ("name", "article", "code", "price_value")
    search_fields = ("name", "article", "code", "price_value")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = [
        ("Основная информация", {"fields": ["name", "article", "code"], "description": "Основные данные о товаре"}),
        (
            "Цены",
            {
                "fields": [
                    ("price_value", "price_currency", "price_type"),
                    ("price2_value", "price2_currency", "price2_type"),
                ],
                "description": "Ценовая информация",
            },
        ),
        ("Характеристики", {"fields": ["vat", "vat_enabled", "weight", "volume"], "description": "Физические характеристики товара"}),
        ("Дополнительно", {"fields": ["barcodes", "payment_item_type", "meta"], "description": "Дополнительная информация"}),
        ("Даты", {"fields": ["created_at", "updated_at"], "description": "Даты создания и обновления"}),
    ]

    list_display = ("name", "article", "code", "price_value")
    list_display_links = ("name",)

    list_filter = ("vat_enabled", "price_currency")

    # Русские заголовки для полей
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return fieldsets
