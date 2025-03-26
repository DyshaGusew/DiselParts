from django.db import models
from django.utils import timezone
from . import ProductPrice


class MoyskladProduct(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    article = models.CharField(max_length=100, blank=True)
    vat = models.IntegerField(default=0)
    vat_enabled = models.BooleanField(default=False)
    weight = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    barcodes = models.JSONField(default=list)
    payment_item_type = models.CharField(max_length=50)
    meta = models.JSONField()
    prices = models.ManyToManyField(ProductPrice)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["article"]),
            models.Index(fields=["code"]),
        ]
