from django.db import models
from . import Currency


class ProductPrice(models.Model):
    value = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    price_type = models.CharField(max_length=100)
