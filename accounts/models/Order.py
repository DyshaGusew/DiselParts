from django.db import models
from .Buyer import Buyer
from catalog.models import ProductForSale
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


def update_order_total(order):
    """Общая функция для обновления суммы заказа"""
    order.total = sum(
        item.quantity * item.Product.sale_price
        for item in order.items.select_related('Product').all()
    )
    order.save(update_fields=['total'])


@receiver(post_save, sender='accounts.OrderItem')
def order_item_saved(sender, instance, **kwargs):
    update_order_total(instance.Order)


@receiver(post_delete, sender='accounts.OrderItem')
def order_item_deleted(sender, instance, **kwargs):
    update_order_total(instance.Order)


class Order(models.Model):
    User = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Покупатель',
    )
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name='Сумма'
    )
    status = models.CharField(
        max_length=50, default='Обрабатывается', verbose_name='Статус'
    )

    def get_date(self):
        return timezone.localtime(self.order_date).strftime('%d.%m.%Y %H:%M')

    def __str__(self):
        return f"Заказ {self.get_date()} от {self.User.username}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
