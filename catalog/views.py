from django.views.generic import ListView, DetailView
from .models import ProductForSale  # Измените импорт


class ProductListView(ListView):
    model = ProductForSale
    template_name = "catalog/list.html"
    context_object_name = "products"  # Исправлено на множественное число
    queryset = ProductForSale.objects.filter(is_active=True)  # Добавьте фильтр


class ProductDetailView(DetailView):
    model = ProductForSale
    template_name = "catalog/detail.html"
    context_object_name = "product"  # Добавлено для ясности
