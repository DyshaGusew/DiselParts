from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import MoyskladProduct
from unfold.admin import ModelAdmin
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


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
                    "border: 1px solid #454545;"  # Цвет границы (можно заменить на var(--unfold-border-color))
                    "border-radius: 0.375rem;"  # Закругление углов
                    "padding: 0.5rem 0.75rem;"  # Внутренние отступы
                    "transition: border-color 0.2s;"  # Плавное изменение цвета
                ),
                "placeholder": "Введите URL изображения",
            }
        ),
        help_text="Форматы: JPG, PNG, WebP",  # Дополнительный текст подсказки
    )

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
    list_filter = ("vat_enabled", "effective_vat_enabled", "archived", "country_name", "price_type", "product_folder_name")
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

        return format_html('<div style="display: flex; flex-wrap: wrap;">{}</div>', mark_safe("".join(images_html))) if images_html else "Нет корректных изображений"

    get_main_image_preview.short_description = "Все изображения товара"

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

    def clean_image_url(self):
        url = self.cleaned_data.get("image_url")
        if url and not url.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            raise ValidationError("Неподдерживаемый формат изображения. Используйте JPG, PNG или WebP.")
        return url

    def save_model(self, request, obj, form, change):
        image_url = form.cleaned_data.get("image_url")

        if image_url:

            new_image = {"original": image_url, "medium": image_url, "thumbnail": image_url}

            if not obj.images:
                obj.images = [new_image]
            else:
                obj.images.append(new_image)

        super().save_model(request, obj, form, change)
