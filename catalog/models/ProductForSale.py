from django.db import models
from config.models.persistent import Persistent
from moysklad.models.MoyskladProduct import MoyskladProduct
import re
from urllib.parse import quote
from django.http import HttpResponse
import requests
from django.conf import settings
from django.utils.text import slugify


class ProductForSale(Persistent):
    moysklad_product = models.OneToOneField(
        MoyskladProduct,
        on_delete=models.CASCADE,
        related_name="for_sale",
        verbose_name="Продукт из МойСклад",
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    article = models.CharField(max_length=100, blank=True, verbose_name="Артикул")
    description = models.TextField(blank=True, verbose_name="Описание")
    group = models.CharField(max_length=255, blank=True, verbose_name="Группа")
    country = models.CharField(max_length=255, blank=True, verbose_name="Страна")
    supplier_legal_title = models.CharField(
        max_length=255, blank=True, verbose_name="Производитель"
    )

    sale_price_moy_sklad = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Цена продажи мойсклад",
        default=0.00,
    )

    # Цена для продажи (может отличаться от цены в МойСклад)
    sale_price = models.DecimalField(
        max_digits=15,
        blank=True,
        null=True,
        decimal_places=2,
        verbose_name="Цена продажи",
        default=0.00,
    )
    markup_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Процент наценки",
        default=0.00,
    )

    is_active = models.BooleanField(default=True, verbose_name="Активен для продажи")

    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")

    class Meta:
        verbose_name = "Товар для продажи"
        verbose_name_plural = "Товары для продажи"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.article}) - {self.sale_price} руб."

    def get_medium_image_url(self):
        return self.moysklad_product.get_medium_image_url()

    def get_original_image_url(self):
        return self.moysklad_product.get_original_image_url()

    def save(self, *args, **kwargs):
        if not self.slug:
            # Генерируем базовый slug из name
            base_slug = slugify(
                f"{self.name}-{self.article}"
                if self.name and self.article
                else self.name
            )
            slug = base_slug
            counter = 1
            # Проверяем уникальность slug
            while ProductForSale.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"  # Добавляем суффикс, если slug занят
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
