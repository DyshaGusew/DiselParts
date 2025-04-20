from django.db import models
from django.contrib.auth.models import AbstractUser


class Buyer(AbstractUser):
    delivery_address = models.TextField(blank=True, verbose_name='Адрес доставки')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
