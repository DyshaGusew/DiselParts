from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import MoyskladProduct
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
    list_display = ("name", "article", "code", "price_value", "vat", "country_name", "is_active", "image_preview")
    list_display_links = ("name", "code", "article")
    search_fields = ("name", "article", "code", "description")
    list_filter = ("vat_enabled", "effective_vat_enabled", "archived", "country_name", "price_type")
    readonly_fields = ("get_main_image_preview",)
    ordering = ("name", "price_value")
    filter_horizontal = ()

    fieldsets = (
        ("Основная информация", {"fields": ("name", "description", ("article", "code", "external_code"))}),
        ("Цены", {"fields": ("price_value", "price_type", "min_price_value", "buy_price_value")}),
        ("Налоги и статус", {"fields": (("vat", "effective_vat"), ("vat_enabled", "effective_vat_enabled", "archived"))}),
        ("Характеристики", {"fields": (("weight", "volume"), "minimum_balance", "barcodes")}),
        (
            "Классификация",
            {
                "fields": ("product_folder_name", "product_folder_description", "country_name"),
                "classes": ("collapse",),
            },
        ),
        (
            "Поставщик",
            {
                "fields": ("supplier_legal_title", "supplier_actual_address", "supplier_phone"),
                "classes": ("collapse",),
            },
        ),
        ("Изображения", {"fields": ("images", "get_main_image_preview")}),
    )

    def get_main_image_preview(self, obj):
        if obj.images:
            img_url = obj.images[0].get("medium") or obj.images[0].get("original")
            if img_url:
                return format_html('<img src="{}" style="max-height: 200px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);"/>', img_url)
        return "Нет изображения"

    get_main_image_preview.short_description = "Превью изображения"

    def image_preview(self, obj):
        if obj.images:
            img_url = obj.images[0].get("medium") or obj.images[0].get("thumbnail")
            if img_url:
                return format_html('<img src="{}" style="height: 50px; border-radius: 5px;"/>', img_url)
        return "-"

    image_preview.short_description = "Миниатюра"

    def is_active(self, obj):
        return not obj.archived

    is_active.boolean = True
    is_active.short_description = "Активен"
