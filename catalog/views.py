from django.views.generic import ListView, DetailView
from .models.ProductForSale import ProductForSale


class ProductListView(ListView):
    model = ProductForSale
    template_name = "catalog/list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = ProductForSale
    template_name = "catalog/detail.html"
