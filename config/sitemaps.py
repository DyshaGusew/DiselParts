from django.contrib.sitemaps import Sitemap
from catalog.models import ProductForSale
from django.urls import reverse


class ProductSitemap(Sitemap):
    changefreq = "weekly"  # Частота обновления страниц
    priority = 0.9  # Приоритет страниц (от 0.0 до 1.0)

    def items(self):
        return ProductForSale.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # Поле с датой последнего обновления

    def location(self, obj):
        return f"/catalog/zapchasti/{obj.slug}/"  # URL страницы товара


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ['home', 'about', 'catalog:product-list']

    def location(self, obj):
        return reverse(obj)
