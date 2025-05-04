from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart-view'),
    path('plus/<int:item_id>/', views.plus_to_cart, name='plus_to_cart'),
    path('minus/<int:item_id>/', views.minus_to_cart, name='minus_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path(
        'update-zquantity/<int:item_id>/', views.update_quantity, name='update-quantity'
    ),
    path('missing_cart', views.MissingCartView.as_view(), name='missing-cart'),
]
