from .models import MoyskladProduct, Currency, ProductPrice
from .api import fetch_products


def sync_with_moysklad():
    """Логика синхронизации"""
    products = fetch_products()
    if not products:
        return False

    for product_data in products:
        # Обработка валюты
        currency, _ = Currency.objects.get_or_create(
            meta_id=product_data["salePrices"][0]["currency"]["meta"]["href"], defaults={"name": product_data["salePrices"][0]["currency"]["meta"].get("name", ""), "code": product_data["salePrices"][0]["currency"]["meta"].get("code", "")}
        )

        # Создание/обновление товара
        product, _ = MoyskladProduct.objects.update_or_create(
            id=product_data["id"],
            defaults={
                "name": product_data["name"],
                "code": product_data.get("code", ""),
                "article": product_data.get("article", ""),
                "vat": product_data.get("vat", 0),
                "vat_enabled": product_data.get("vatEnabled", False),
                "weight": product_data.get("weight", 0.0),
                "volume": product_data.get("volume", 0.0),
                "barcodes": [b["ean13"] for b in product_data.get("barcodes", [])],
                "payment_item_type": product_data.get("paymentItemType", "GOOD"),
                "meta": product_data["meta"],
            },
        )

        # Обработка цен
        for price_data in product_data.get("salePrices", []):
            ProductPrice.objects.update_or_create(product=product, price_type=price_data["priceType"]["name"], defaults={"value": price_data["value"], "currency": currency})

    return True
