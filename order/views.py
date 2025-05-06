from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Basket, BasketItem, OrderItem, Order
from catalog.models import ProductForSale
from django.db import transaction
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse


@login_required
def cart_view(request):
    basket, created = Basket.objects.get_or_create(User=request.user)

    context = {
        'basket': basket,
    }
    return render(request, 'order/cart.html', context)


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
def update_quantity_from_cart(request, item_id):
    basket_item = get_object_or_404(BasketItem, pk=item_id, Basket__User=request.user)
    action = request.POST.get('action')

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

    return redirect('order:cart-view')


@login_required
def update_quantity_from_list(request, item_id):
    if request.method == 'POST':
        try:
            current_params = request.POST.get('current_params', '')

            basket = request.user.basket.first()
            if not basket:
                basket = Basket.objects.create(user=request.user)

            product = get_object_or_404(ProductForSale, pk=item_id)

            basket_item, created = BasketItem.objects.get_or_create(
                Basket=basket, Product=product, defaults={'quantity': 0}
            )

            if request.POST.get('action') == 'add':
                quantity = int(request.POST.get('quantity', 1))
                basket_item.quantity += quantity
                basket_item.save()

                messages.success(
                    request, f'Добавлено "{product.name}" ({quantity} шт.) в корзину.'
                )

            base_url = reverse('catalog:product-list')
            redirect_url = f"{base_url}?{current_params}"
            return redirect(redirect_url)

        except ValueError:
            messages.error(request, 'Некорректное количество')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            print(f'Ошибка: {str(e)}')

    return redirect('catalog:product-list')


@login_required
def update_quantity_from_product(request, item_id):
    if request.method == 'POST':
        try:
            basket = request.user.basket.first()
            if not basket:
                basket = Basket.objects.create(user=request.user)

            product = get_object_or_404(ProductForSale, pk=item_id)

            basket_item, created = BasketItem.objects.get_or_create(
                Basket=basket, Product=product, defaults={'quantity': 0}
            )

            if request.POST.get('action') == 'add':
                quantity = int(request.POST.get('quantity', 1))
                basket_item.quantity += quantity
                basket_item.save()

                messages.success(
                    request, f'Добавлено "{product.name}" ({quantity} шт.) в корзину.'
                )

            return redirect('catalog:product-detail', pk=product.id)

        except ValueError:
            messages.error(request, 'Некорректное количество')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')
            print(f'Ошибка: {str(e)}')

    return redirect('catalog:product-list')


@login_required
def create_order(request):
    try:
        # Получаем корзину пользователя
        basket, create = Basket.objects.get_or_create(User=request.user)
        basket_items = basket.items.all()

        if not basket_items.exists():
            messages.error(request, 'Ваша корзина пуста')
            return redirect('order:cart-view')

        # Создаем новый заказ
        with transaction.atomic():
            order = Order.objects.create(User=request.user, status='Обрабатывается')
            for basket_item in basket_items:
                OrderItem.objects.create(
                    Order=order,
                    Product=basket_item.Product,
                    quantity=basket_item.quantity,
                )

            basket.items.all().delete()
            basket.total = 0
            basket.products_count = 0
            basket.save()

            messages.success(request, 'Заказ успешно создан!')
            return redirect('accounts:profile')

    except Basket.DoesNotExist:
        print(f"Ошибка: Корзина не найдена для пользователя {request.user.email}")
        messages.error(request, 'Корзина не найдена')
        return redirect('order:cart-view')
    except Exception as e:
        print(f"Ошибка при создании заказа: {str(e)}")
        messages.error(request, 'Произошла ошибка при создании заказа')
        return redirect('order:cart-view')
