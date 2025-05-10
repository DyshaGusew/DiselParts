from django.urls import path
from .views import ProductListView, ProductDetailView, proxy_product_image


urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path(
        'zapchasti/<slug:slug>/',
        ProductDetailView.as_view(),
        name='product-detail',
    ),
    path(
        'product/<str:product_id>/image/<int:image_index>/',
        proxy_product_image,
        name='proxy_product_image',
    ),
]
