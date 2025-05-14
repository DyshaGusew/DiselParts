from django.db import models
from accounts.models.Buyer import Buyer
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


@receiver(post_save, sender='order.OrderItem')
def order_item_saved(sender, instance, **kwargs):
    update_order_total(instance.Order)


@receiver(post_delete, sender='order.OrderItem')
def order_item_deleted(sender, instance, **kwargs):
    update_order_total(instance.Order)


class Order(models.Model):
    STATUS_CHOICES = [
        ('Обрабатывается', 'Обрабатывается'),
        ('Ожидает оплаты', 'Ожидает оплаты'),
        ('Отправлен', 'Отправлен'),
        ('Доставлен', 'Доставлен'),
        ('Отменен', 'Отменен'),
        ('Другое', 'Другое'),
    ]
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
        max_length=255,
        choices=STATUS_CHOICES,
        default='Обрабатывается',
        verbose_name='Статус',
    )
    other_info = models.TextField(blank=True, verbose_name="Дополнительная информация")

    def get_date(self):
        return timezone.localtime(self.order_date).strftime('%d.%m.%Y %H:%M')

    def __str__(self):
        return f"Заказ {self.get_date()} от {self.User.email}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
