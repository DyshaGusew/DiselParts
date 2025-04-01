from .models import MoyskladProduct
import requests
from django.conf import settings


def fetch_products() -> dict:
    """Получение товаров из API МойСклад"""
    try:
        response = requests.get("https://api.moysklad.ru/api/remap/1.2/entity/product", headers={"Authorization": f"Bearer {settings.MOYSKLAD_TOKEN}", "Accept-Encoding": "gzip"}, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка API: {str(e)}")
        return None


def sync_products_with_moysklad() -> bool:
    """Основная логика синхронизации товаров"""
    products_data = fetch_products()
    if not products_data:
        print("Не удалось получить данные из API")
        return False

    if "rows" not in products_data:
        print("Некорректный формат ответа API: отсутствует ключ 'rows'")
        return False

    success_count, error_count = 0, 0

    for product_data in products_data["rows"]:
        try:
            if not product_data.get("salePrices"):
                print(f"Товар {product_data.get('id')} не имеет цен, пропускаем")
                continue

            # Получаем данные основной цены (первой в списке)
            main_price = product_data["salePrices"][0] if product_data["salePrices"] else {}
            price_currency_code = main_price.get("currency", {}).get("meta", {}).get("code", "RUB")

            # Создание/обновление товара
            product, _ = MoyskladProduct.objects.update_or_create(
                id=product_data["id"],
                defaults={
                    "name": product_data.get("name", ""),
                    "code": product_data.get("code", ""),
                    "article": product_data.get("article", ""),
                    "vat": product_data.get("vat", 0),
                    "vat_enabled": product_data.get("vatEnabled", False),
                    "weight": product_data.get("weight", 0.0),
                    "volume": product_data.get("volume", 0.0),
                    "barcodes": [b.get("ean13") for b in product_data.get("barcodes", []) if b.get("ean13")],
                    "payment_item_type": product_data.get("paymentItemType", "GOOD"),
                    "meta": product_data.get("meta", {}),
                    "price_value": main_price.get("value", 0) / 100,  # Конвертируем копейки в рубли
                    "price_currency": price_currency_code,
                    "price_type": main_price.get("priceType", {}).get("name", ""),
                    # Аналогично для price2_* если нужно
                },
            )

            success_count += 1

        except Exception as e:
            error_count += 1
            print(f"Ошибка обработки товара {product_data.get('id')}: {str(e)}")
            continue

    print(f"\nСинхронизация завершена. Успешно: {success_count}, Ошибок: {error_count}")
    return error_count == 0
