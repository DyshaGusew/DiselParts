from django.db import models
from .Basket import Basket
from catalog.models import ProductForSale
from django.core.validators import MinValueValidator


class BasketItem(models.Model):
    Basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина',
    )
    Product = models.ForeignKey(
        ProductForSale,
        on_delete=models.CASCADE,
        related_name='basket_items',
        verbose_name='Продукт',
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], verbose_name='Кол-во'
    )

    def __str__(self):
        return f"{self.Product.name} x{self.quantity} в {self.Basket}"

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
