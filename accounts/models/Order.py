from django.db import models
from .Buyer import Buyer
from catalog.models import ProductForSale


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

    def __str__(self):
        return f"Заказ #{self.id} от {self.User.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total = sum(
            item.quantity * item.order_items.sale_price for item in self.items.all()
        )
        super().save(update_fields=['total'])

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
