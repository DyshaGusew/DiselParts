from django.db import models
from config.models.persistent import Persistent
from moysklad.models.MoyskladProduct import MoyskladProduct


class ProductForSale(Persistent):
    # Связь с оригинальным товаром
    moysklad_product = models.OneToOneField(
        MoyskladProduct, on_delete=models.CASCADE, related_name="for_sale"
    )

    # Основные поля (дублируем только нужные)
    name = models.CharField(max_length=255, verbose_name="Название")
    article = models.CharField(max_length=100, blank=True, verbose_name="Артикул")
    description = models.TextField(blank=True, verbose_name="Описание")

    # Цена для продажи (может отличаться от цены в МойСклад)
    sale_price = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="Цена продажи"
    )

    # Дополнительные поля для продажи
    is_active = models.BooleanField(default=True, verbose_name="Активен для продажи")

    # Дополнительные поля, специфичные для вашего приложения
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")

    class Meta:
        verbose_name = "Товар для продажи"
        verbose_name_plural = "Товары для продажи"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.article}) - {self.sale_price} руб."

    def get_main_image_url(self):
        """Делегируем метод оригинальной модели"""
        return self.moysklad_product.get_main_image_url()
