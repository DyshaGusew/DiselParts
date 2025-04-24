from django.db import models
from accounts.models.Buyer import Buyer
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


def update_basket_total(basket):
    """Общая функция для обновления суммы и количества в корзине"""
    basket.total = sum(
        item.quantity * item.Product.sale_price
        for item in basket.items.select_related('Product').all()
    )
    basket.products_count = sum(
        item.quantity for item in basket.items.select_related('Product').all()
    )
    basket.save(update_fields=['total', 'products_count'])


@receiver(post_save, sender='order.BasketItem')
def basket_item_saved(sender, instance, **kwargs):
    update_basket_total(instance.Basket)


@receiver(post_delete, sender='order.BasketItem')
def basket_item_deleted(sender, instance, **kwargs):
    update_basket_total(instance.Basket)


class Basket(models.Model):
    User = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE,
        related_name='busket',
        verbose_name='Покупатель',
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name='Сумма'
    )
    products_count = models.PositiveIntegerField(
        default=0, verbose_name='Кол-во товаров'
    )

    def __str__(self):
        return f"Корзина от {self.User.email}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
