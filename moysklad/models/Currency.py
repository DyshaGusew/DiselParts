from django.db import models


class Currency(models.Model):
    meta_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)
