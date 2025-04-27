from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Basket, BasketItem
from catalog.models import ProductForSale
from django.db import transaction
from django.views.generic import TemplateView


@login_required
def cart_view(request):
    basket, created = Basket.objects.get_or_create(User=request.user)

    context = {
        'basket': basket,
    }
    return render(request, 'order/cart.html', context)


@login_required
def update_quantity(request, item_id):
    if request.method == 'POST':
        basket_item = get_object_or_404(
            BasketItem, pk=item_id, Basket__User=request.user
        )
        action = request.POST.get('action')

        if action == 'increase':
            basket_item.quantity += 1
        elif action == 'decrease':
            if basket_item.quantity > 1:
                basket_item.quantity -= 1
        else:  # Если нажата кнопка обновления или изменено значение вручную
            try:
                new_quantity = int(request.POST.get('quantity', 1))
                if new_quantity >= 1:
                    basket_item.quantity = new_quantity
            except (ValueError, TypeError):
                pass  # Оставляем текущее значение при ошибке

        basket_item.save()

    return redirect('order:cart_view')


@login_required
def plus_to_cart(request, item_id):
    basket_item = get_object_or_404(BasketItem, pk=item_id, Basket__User=request.user)
    basket_item.quantity += 1
    basket_item.save()

    return redirect('order:cart-view')


@login_required
def minus_to_cart(request, item_id):
    basket_item = get_object_or_404(BasketItem, pk=item_id, Basket__User=request.user)
    if basket_item.quantity > 1:
        basket_item.quantity -= 1
    else:
        basket_item.delete()
        return redirect('order:cart-view')

    basket_item.save()

    return redirect('order:cart-view')


@login_required
def remove_from_cart(request, item_id):
    basket_item = get_object_or_404(BasketItem, pk=item_id, Basket__User=request.user)
    basket_item.delete()
    return redirect('order:cart-view')


@login_required
def update_quantity(request, item_id):
    basket_item = get_object_or_404(BasketItem, pk=item_id, Basket__User=request.user)
    action = request.POST.get('action')
    quantity_form = request.POST.get('quantity')

    with transaction.atomic():
        if action == 'increase':
            basket_item.quantity += 1
        elif action == 'decrease' and basket_item.quantity > 1:
            basket_item.quantity -= 1
        else:
            try:
                new_quantity = int(request.POST.get('quantity', 1))
                print(new_quantity)
                if new_quantity >= 1:
                    basket_item.quantity = new_quantity
            except (ValueError, TypeError):
                pass  # Оставляем текущее значение при ошибке
        basket_item.save()

    basket = Basket.objects.get(User=request.user)
    return redirect('order:cart-view')


class MissingCartView(TemplateView):
    template_name = 'order/missing_cart.html'
