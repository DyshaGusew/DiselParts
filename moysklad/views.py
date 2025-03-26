from django.http import JsonResponse
from .api import fetch_products


def product_list(request):
    data = fetch_products()
    if data:
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "API недоступно"}, status=500)
