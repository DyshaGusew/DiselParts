from django.db import models


class Persistent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    aka = models.CharField("Наименование", max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.aka}"

    class Meta:
        abstract = True
