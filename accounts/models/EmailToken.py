import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta


class EmailToken(models.Model):
    buyer = models.ForeignKey(
        'Buyer',
        on_delete=models.CASCADE,
        verbose_name=("Пользователь"),
        related_name='buyers',
    )
    token = models.CharField(
        max_length=100, unique=True, default=uuid.uuid4, verbose_name=("Токен")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("Дата создания"))
    is_used = models.BooleanField(default=False, verbose_name=("Использован"))

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(hours=24)

    def __str__(self):
        return f"Токен для {self.buyer.email}"

    class Meta:
        verbose_name = "Токен верификации email"
        verbose_name_plural = "Токены верификации email"
