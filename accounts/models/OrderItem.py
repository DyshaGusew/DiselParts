from django.db import models
from .Order import Order
from catalog.models import ProductForSale
from django.core.validators import MinValueValidator


class OrderItem(models.Model):
    Order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ',
    )
    Product = models.ForeignKey(
        ProductForSale,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Продукт',
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], verbose_name='Кол-во'
    )

    def __str__(self):
        return f"{self.Product.name} x{self.quantity} в {self.Order}"

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
