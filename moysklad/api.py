import requests
from django.conf import settings

BASE_URL = "https://api.moysklad.ru/api/remap/1.2/"


def fetch_products():
    """Основная функция для загрузки данных"""
    try:
        response = requests.get("https://api.moysklad.ru/api/remap/1.2/entity/product", headers={"Authorization": f"Bearer {settings.MOYSKLAD_TOKEN}", "Accept-Encoding": "gzip"}, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API Error: {str(e)}")
        return None
