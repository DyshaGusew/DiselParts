from django.db import models
from config.models.persistent import Persistent


class MoyskladProduct(Persistent):
    # Основные поля
    id = models.CharField(primary_key=True, max_length=255, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Мяу")
    code = models.CharField(max_length=100, blank=True, verbose_name="Код")
    article = models.CharField(max_length=100, blank=True, verbose_name="Артикул")
    external_code = models.CharField(max_length=100, blank=True, verbose_name="Внешний код")
    description = models.TextField(blank=True, verbose_name="Описание")

    # Налоговая информация
    vat = models.IntegerField(default=0, verbose_name="НДС")
    effective_vat = models.IntegerField(default=0, verbose_name="Эффективный НДС")
    effective_vat_enabled = models.BooleanField(default=False, verbose_name="Эффективный НДС включен")
    vat_enabled = models.BooleanField(default=False, verbose_name="НДС включен")

    # Статус
    archived = models.BooleanField(default=False, verbose_name="В архиве")

    # Физические характеристики
    weight = models.FloatField(default=0.0, verbose_name="Вес")
    volume = models.FloatField(default=0.0, verbose_name="Объем")
    minimum_balance = models.FloatField(default=0.0, verbose_name="Минимальный остаток")

    # Идентификаторы
    barcodes = models.JSONField(default=list, verbose_name="Штрихкоды")
    payment_item_type = models.CharField(max_length=50, default="GOOD", verbose_name="Тип оплаты")

    # Цены
    price_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Цена")
    price_type = models.CharField(max_length=100, blank=True, verbose_name="Тип цены")

    min_price_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Минимальная цена")

    buy_price_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Закупочная цена")

    # Связанные объекты (названия)
    product_folder_name = models.CharField(max_length=255, blank=True, verbose_name="Название группы")
    product_folder_description = models.TextField(blank=True, verbose_name="Описание группы")
    country_name = models.CharField(max_length=100, blank=True, verbose_name="Страна")

    # Поставщик
    supplier_legal_title = models.CharField(max_length=255, blank=True, verbose_name="Юр. название поставщика")
    supplier_actual_address = models.TextField(blank=True, verbose_name="Фактический адрес поставщика")
    supplier_phone = models.CharField(max_length=50, blank=True, verbose_name="Телефон поставщика")

    # Изображения (храним как JSON)
    images = models.JSONField(default=list, verbose_name="Изображения")

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

    def get_main_image_url(self):
        """Возвращает URL основного изображения или None"""
        if self.images and len(self.images) > 0:
            return self.images[0].get("medium") or self.images[0].get("original")
        return None
