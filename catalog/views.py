from click import group
from django.views.generic import ListView, DetailView
from .models import ProductForSale
from django.views.generic import ListView
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
import requests


def get_product_images(product_id: str) -> list:
    """Получение изображений товара"""
    url = f"https://api.moysklad.ru/api/remap/1.2/entity/product/{product_id}/images"
    try:
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {settings.MOYSKLAD_TOKEN}",
                "Accept-Encoding": "gzip",
            },
            timeout=10,
        )
        response.raise_for_status()
        images_data = response.json()

        images = []
        for img in images_data.get("rows", []):
            images.append(
                {
                    "original": img["meta"]["downloadHref"],
                    "medium": img.get("miniature", {}).get("downloadHref", ""),
                    "thumbnail": img.get("tiny", {}).get("href", ""),
                }
            )
        return images

    except Exception as e:
        print(f"Ошибка получения изображений для товара {product_id}: {str(e)}")
        return []


def proxy_product_image(request, product_id, image_index=0):
    """Проксирует оригинальное изображение из МойСклад"""
    # Получаем изображения для товара
    images = get_product_images(product_id)

    if not images or len(images) <= image_index:
        return HttpResponse(status=404)  # Изображение не найдено

    image_url = images[image_index].get("original")
    if not image_url:
        return HttpResponse(status=404)

    try:
        # Запрашиваем изображение с авторизацией
        response = requests.get(
            image_url,
            headers={
                "Authorization": f"Bearer {settings.MOYSKLAD_TOKEN}",
                "Accept-Encoding": "gzip",
            },
            timeout=10,
            stream=True,
        )
        response.raise_for_status()

        # Возвращаем изображение клиенту
        content_type = response.headers.get("content-type", "image/jpeg")
        response = HttpResponse(response.content, content_type=content_type)
        response['Cache-Control'] = 'public, max-age=604800'  # Кэш на 7 дней
        return response

    except requests.exceptions.RequestException as e:
        print(f"Ошибка загрузки изображения: {str(e)}")
        return HttpResponse(status=500)


class ProductListView(ListView):
    model = ProductForSale
    template_name = "catalog/list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = ProductForSale.objects.filter(is_active=True)

        # Поиск
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(article__icontains=search_query)
            )

        # Фильтрация по стране
        country = self.request.GET.get('country')
        if country:
            queryset = queryset.filter(country=country)

        # Фильтрация по группе
        group = self.request.GET.get('group')
        if group:
            queryset = queryset.filter(group=group)

        # Фильтрация по производителю
        manufacturer = self.request.GET.get('manufacturer')
        if manufacturer:
            queryset = queryset.filter(supplier_legal_title=manufacturer)

        # Сортировка
        sort = self.request.GET.get('sort', 'name')
        if sort == 'price_asc':
            queryset = queryset.order_by('sale_price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-sale_price')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем параметры фильтрации
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_country'] = self.request.GET.get('country', '')
        context['selected_manufacturer'] = self.request.GET.get('manufacturer', '')
        context['selected_group'] = self.request.GET.get('group', '')
        context['selected_sort'] = self.request.GET.get('sort', 'name')

        # Получаем уникальные значения для фильтров
        context['countries'] = (
            ProductForSale.objects.filter(is_active=True, country__isnull=False)
            .exclude(country='')
            .order_by('country')
            .values_list('country', flat=True)
            .distinct()
        )

        context['manufacturers'] = (
            ProductForSale.objects.filter(
                is_active=True, supplier_legal_title__isnull=False
            )
            .exclude(supplier_legal_title='')
            .order_by('supplier_legal_title')
            .values_list('supplier_legal_title', flat=True)
            .distinct()
        )

        context['groups'] = (
            ProductForSale.objects.filter(is_active=True, group__isnull=False)
            .exclude(group='')
            .order_by('group')
            .values_list('group', flat=True)
            .distinct()
        )

        # Варианты сортировки
        context['sort_options'] = [
            {'value': 'name', 'label': 'По названию'},
            {'value': 'price_asc', 'label': 'Цена по возрастанию'},
            {'value': 'price_desc', 'label': 'Цена по убыванию'},
            {'value': 'newest', 'label': 'Новые первыми'},
        ]

        return context


class ProductDetailView(DetailView):
    model = ProductForSale
    template_name = "catalog/detail.html"
    context_object_name = "product"
