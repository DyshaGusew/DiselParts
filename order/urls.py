from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart-view'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path(
        'update-quantity/<int:item_id>/',
        views.update_quantity_from_cart,
        name='update-quantity',
    ),
    path(
        'update-quantity-list/<int:item_id>/',
        views.update_quantity_from_list,
        name='update-quantity-list',
    ),
    path(
        'update-quantity-product/<int:item_id>/',
        views.update_quantity_from_product,
        name='update-quantity-product',
    ),
    path('create-order', views.create_order, name='create-order'),
]
