from django.db import models
from config.models.persistent import Persistent
from django.core.cache import cache


class MoyskladProduct(Persistent):
    # Основные поля
    id = models.CharField(primary_key=True, max_length=255, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название")
    moysklad_url = models.URLField(
        "Ссылка в МойСклад",
        max_length=500,
        blank=True,
        help_text="Прямая ссылка на товар в интерфейсе МойСклад",
    )
    code = models.CharField(max_length=100, blank=True, verbose_name="Код")
    article = models.CharField(max_length=100, blank=True, verbose_name="Артикул")
    external_code = models.CharField(
        max_length=100, blank=True, verbose_name="Внешний код"
    )
    description = models.TextField(blank=True, verbose_name="Описание")

    # Налоговая информация
    vat = models.IntegerField(default=0, verbose_name="НДС")
    effective_vat = models.IntegerField(
        default=0, blank=True, verbose_name="Эффективный НДС"
    )
    effective_vat_enabled = models.BooleanField(
        default=False, verbose_name="Эффективный НДС включен"
    )
    vat_enabled = models.BooleanField(default=False, verbose_name="НДС включен")

    # Статус
    archived = models.BooleanField(default=False, verbose_name="В архиве")

    # Физические характеристики
    weight = models.FloatField(default=0.0, blank=True, verbose_name="Вес")
    volume = models.FloatField(default=0.0, blank=True, verbose_name="Объем")
    minimum_balance = models.FloatField(
        default=0.0, blank=True, verbose_name="Минимальный остаток"
    )

    # Идентификаторы
    barcodes = models.JSONField(default=list, blank=True, verbose_name="Штрихкоды")
    payment_item_type = models.CharField(
        max_length=50, default="GOOD", verbose_name="Тип оплаты"
    )

    # Цены
    price_value = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, verbose_name="Цена"
    )
    price_type = models.CharField(max_length=100, blank=True, verbose_name="Тип цены")

    min_price_value = models.DecimalField(
        max_digits=15,
        blank=True,
        decimal_places=2,
        default=0,
        verbose_name="Минимальная цена",
    )

    buy_price_value = models.DecimalField(
        max_digits=15,
        blank=True,
        decimal_places=2,
        default=0,
        verbose_name="Закупочная цена",
    )

    # Связанные объекты (названия)
    product_folder_name = models.CharField(
        max_length=255, default="Основная", blank=True, verbose_name="Название группы"
    )
    product_folder_description = models.TextField(
        blank=True, verbose_name="Описание группы"
    )
    country_name = models.CharField(max_length=100, blank=True, verbose_name="Страна")

    # Поставщик
    supplier_legal_title = models.CharField(
        max_length=255, blank=True, verbose_name="Поставщик"
    )
    supplier_actual_address = models.TextField(
        blank=True, verbose_name="Фактический адрес поставщика"
    )
    supplier_phone = models.CharField(
        max_length=50, blank=True, verbose_name="Телефон поставщика"
    )

    images = models.JSONField(default=list, blank=True, verbose_name="Изображения")

    medium_image = models.ImageField(
        upload_to='products/medium/', null=True, blank=True
    )
    original_image = models.ImageField(
        upload_to='products/original/', null=True, blank=True
    )

    class Meta:
        verbose_name = "Товар МойСклад"
        verbose_name_plural = "Товары МойСклад"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["article"]),
            models.Index(fields=["code"]),
            models.Index(fields=["price_value"]),
            models.Index(fields=["archived"]),
        ]
        ordering = ["name"]

    def __str__(self):
        display_name = self.name
        if self.article:
            display_name += f" ({self.article})"
        elif self.code:
            display_name += f" ({self.code})"
        return display_name

    def get_medium_image_url(self):
        """Возвращает URL локального среднего изображения с кэшированием"""
        cache_key = f'medium_image_url_{self.id}'
        image_url = cache.get(cache_key)
        if image_url is None:
            if self.medium_image:
                image_url = self.medium_image.url
            elif self.images and len(self.images) > 0:
                image_url = self.images[0].get("medium")
            else:
                image_url = ''
            cache.set(cache_key, image_url, 60 * 60 * 24)
        return image_url or None

    def get_original_image_url(self):
        """Возвращает URL локального оригинального изображения с кэшированием"""
        cache_key = f'original_image_url_{self.id}'
        image_url = cache.get(cache_key)
        if image_url is None:
            if self.original_image:
                image_url = self.original_image.url
            elif self.images and len(self.images) > 0:
                image_url = self.images[0].get("original")
            else:
                image_url = ''
            cache.set(cache_key, image_url, 60 * 60 * 24)
        return image_url or None
