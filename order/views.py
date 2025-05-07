from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from config import settings
from django.utils import timezone

from .models import Basket, BasketItem, OrderItem, Order
from catalog.models import ProductForSale
from django.db import transaction
from django.contrib import messages


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

        missing_fields = []
        if (
            not request.user.delivery_address
            or request.user.delivery_address.strip() == ''
        ):
            missing_fields.append('адрес доставки')
        if not request.user.phone or request.user.phone.strip() == '':
            missing_fields.append('номер телефона')
        if not request.user.email or request.user.email.strip() == '':
            missing_fields.append('email')

        if missing_fields:
            from django.utils.safestring import mark_safe

            fields_str = ", ".join(missing_fields)
            messages.error(
                request,
                mark_safe(
                    f'Для оформления заказа необходимо указать в <a href="{reverse("accounts:edit_profile")}" class="alert-link">профиле</a>: {fields_str}'
                ),
            )
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

            order_items = []
            for order_item in order.items.all():
                item_total = order_item.quantity * order_item.Product.sale_price
                order_items.append(
                    f"• {order_item.Product.name} - "
                    f"{order_item.quantity} шт. x {order_item.Product.sale_price} ₽ = "
                    f"{item_total} ₽"
                )

            order_date = timezone.localtime(order.order_date).strftime(
                '%d.%m.%Y в %H:%M'
            )

            send_mail(
                subject=f"Новый заказ №{order.id} от {order_date}",
                message=(
                    f"Детали заказа:\n"
                    f"Клиент: {order.User.email}\n"
                    f"Дата: {order_date}\n"
                    f"Сумма заказа: {order.total} ₽\n\n"
                    "Состав заказа:\n"
                    + "\n".join(order_items)
                    + "\n\n"
                    + f"Адрес доставки: {request.user.delivery_address}\n"
                    f"Телефон: {request.user.phone}"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.DEFAULT_TO_EMAIL],
                fail_silently=False,
            )

            messages.success(request, f'Заказ на сумму {order.total} успешно создан!')
            return redirect('accounts:profile')

    except Basket.DoesNotExist:
        print(f"Ошибка: Корзина не найдена для пользователя {request.user.email}")
        messages.error(request, 'Корзина не найдена')
        return redirect('order:cart-view')
    except Exception as e:
        print(f"Ошибка при создании заказа: {str(e)}")
        messages.error(
            request, 'Произошла ошибка при создании заказа позвоните в поддежку'
        )
        return redirect('order:cart-view')
