from django.db import models
from django.utils import timezone
from config.models.persistent import Persistent


class MoyskladProduct(Persistent):
    id = models.CharField(primary_key=True, max_length=255, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название")
    code = models.CharField(max_length=100, blank=True, verbose_name="Код")
    article = models.CharField(max_length=100, blank=True, verbose_name="Артикул")
    vat = models.IntegerField(default=0, verbose_name="НДС")
    vat_enabled = models.BooleanField(default=False, verbose_name="НДС включен")
    weight = models.FloatField(default=0.0, verbose_name="Вес")
    volume = models.FloatField(default=0.0, verbose_name="Объем")
    barcodes = models.JSONField(default=list, verbose_name="Штрихкоды")
    payment_item_type = models.CharField(max_length=50, verbose_name="Тип оплаты")
    meta = models.JSONField(verbose_name="Метаданные")

    # Поля для цен
    price_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Цена")
    price_currency = models.CharField(max_length=3, blank=True, verbose_name="Валюта цены")
    price_type = models.CharField(max_length=100, blank=True, verbose_name="Тип цены")

    # Дополнительные поля цен
    price2_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, verbose_name="Цена 2")
    price2_currency = models.CharField(max_length=3, blank=True, verbose_name="Валюта цены 2")
    price2_type = models.CharField(max_length=100, blank=True, verbose_name="Тип цены 2")

    class Meta:
        verbose_name = "Товар МойСклад"
        verbose_name_plural = "Товары МойСклад"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["article"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.article})"
