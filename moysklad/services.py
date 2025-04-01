from .models import MoyskladProduct
import requests
from django.conf import settings
import re
from django.db.models import Q


def fetch_products() -> dict:
    """Получение товаров из API МойСклад"""
    try:
        response = requests.get("https://api.moysklad.ru/api/remap/1.2/entity/product", headers={"Authorization": f"Bearer {settings.MOYSKLAD_TOKEN}", "Accept-Encoding": "gzip"}, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка API: {str(e)}")
        return None


def fetch_additional_data(url: str) -> dict:
    """Получение дополнительных данных по ссылке из МойСклад"""
    try:
        response = requests.get(url, headers={"Authorization": f"Bearer {settings.MOYSKLAD_TOKEN}", "Accept-Encoding": "gzip"}, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка получения данных по ссылке {url}: {str(e)}")
        return {}


def extract_id_from_href(href: str) -> str:
    """Извлекает ID из поля href в формате URL"""
    if not href:
        return ""
    parts = href.rstrip("/").split("/")
    return parts[-1] if parts else ""


def process_price(price_data: dict) -> tuple:
    """Обрабатывает данные о цене, возвращает значение"""
    value = price_data.get("value", 0)
    return value


def process_linked_object(data: dict, field: str) -> str:
    """Извлекает ID связанного объекта по названию поля"""
    obj_data = data.get(field, {})
    href = obj_data.get("meta", {}).get("href", "")
    return extract_id_from_href(href)


def get_product_folder_info(folder_id: str) -> dict:
    """Получение информации о группе товаров"""
    if not folder_id:
        return {"name": "", "description": ""}

    url = f"https://api.moysklad.ru/api/remap/1.2/entity/productfolder/{folder_id}"
    data = fetch_additional_data(url)

    return {"name": data.get("name", ""), "description": data.get("description", "")}


def get_country_info(country_id: str) -> str:
    """Получение названия страны"""
    if not country_id:
        return ""

    url = f"https://api.moysklad.ru/api/remap/1.2/entity/country/{country_id}"
    data = fetch_additional_data(url)
    return data.get("name", "")


def get_product_images(product_id: str) -> list:
    """Получение изображений товара"""
    url = f"https://api.moysklad.ru/api/remap/1.2/entity/product/{product_id}/images"
    try:
        response = requests.get(url, headers={"Authorization": f"Bearer {settings.MOYSKLAD_TOKEN}", "Accept-Encoding": "gzip"}, timeout=10)
        response.raise_for_status()
        images_data = response.json()

        images = []
        for img in images_data.get("rows", []):
            images.append({"original": img["meta"]["downloadHref"], "medium": img.get("miniature", {}).get("downloadHref", ""), "thumbnail": img.get("tiny", {}).get("href", "")})
        return images

    except Exception as e:
        print(f"Ошибка получения изображений для товара {product_id}: {str(e)}")
        return []


def get_supplier_info(supplier_id: str) -> dict:
    """Получение информации о поставщике"""
    if not supplier_id:
        return {"legal_title": "", "actual_address": "", "phone": ""}

    url = f"https://api.moysklad.ru/api/remap/1.2/entity/organization/{supplier_id}"
    data = fetch_additional_data(url)

    return {"legal_title": data.get("legalTitle", ""), "actual_address": data.get("actualAddress", ""), "phone": data.get("phone", "")}


def extract_article_number(name: str) -> str:
    """Извлекает артикул из названия товара"""
    # Основной шаблон для артикула с тире
    match = re.search(r"\b[\w\d]+(?:-[\w\d]+)+\b", name)
    if match:
        return match.group(0)

    # Дополнительный шаблон для артикула без тире
    match = re.search(r"\b[A-Z]?\d+[A-Z]?\d*\b", name)
    return match.group(0) if match else ""


def get_or_create_article(product_data: dict) -> dict:
    """Основная функция обработки артикулов"""
    article = product_data.get("article", "")
    name = product_data.get("name", "")

    if article:
        return product_data

    extracted_article = extract_article_number(name)

    if extracted_article:
        exists = MoyskladProduct.objects.filter(Q(article=extracted_article) | Q(code=extracted_article)).exists()

        if not exists:
            product_data["article"] = extracted_article

    return product_data


def extract_product_defaults(product_data: dict) -> dict:
    """Извлекает и преобразует данные товара в формат для модели"""
    product_id = product_data["id"]
    images = get_product_images(product_id)
    main_price = product_data.get("salePrices", [{}])[0]
    min_price = product_data.get("minPrice", {})
    buy_price = product_data.get("buyPrice", {})

    # Обработка цен
    price_value = process_price(main_price)
    min_price_value = process_price(min_price)
    buy_price_value = process_price(buy_price)

    # Обработка связанных объектов
    supplier_id = process_linked_object(product_data, "supplier")
    country_id = process_linked_object(product_data, "country")
    product_folder_id = process_linked_object(product_data, "productFolder")

    # Получение дополнительных данных
    product_folder_info = get_product_folder_info(product_folder_id)
    country_name = get_country_info(country_id)
    supplier_info = get_supplier_info(supplier_id)

    # Обрабатываем артикул
    product_data = get_or_create_article(product_data)
    return {
        # Основная информация
        "name": product_data.get("name", ""),
        "code": product_data.get("code", ""),
        "external_code": product_data.get("externalCode", ""),
        "description": product_data.get("description", ""),
        "article": product_data.get("article", ""),
        # Налоговая информация
        "vat": product_data.get("vat", 0),
        "effective_vat": product_data.get("effectiveVat", 0),
        "effective_vat_enabled": product_data.get("effectiveVatEnabled", False),
        "vat_enabled": product_data.get("vatEnabled", False),
        # Статус
        "archived": product_data.get("archived", False),
        # Физические характеристики
        "weight": product_data.get("weight", 0.0),
        "volume": product_data.get("volume", 0.0),
        "minimum_balance": product_data.get("minimumBalance", 0.0),
        # Идентификаторы
        "barcodes": [b.get("ean13") for b in product_data.get("barcodes", []) if b.get("ean13")],
        "payment_item_type": product_data.get("paymentItemType", "GOOD"),
        # Цены
        "price_value": price_value / 100,
        "price_type": main_price.get("priceType", {}).get("name", ""),
        "min_price_value": min_price_value / 100,
        "buy_price_value": buy_price_value / 100,
        # Дополнительная информация
        "product_folder_name": product_folder_info["name"],
        "product_folder_description": product_folder_info["description"],
        "country_name": country_name,
        "supplier_legal_title": supplier_info["legal_title"],
        "supplier_actual_address": supplier_info["actual_address"],
        "supplier_phone": supplier_info["phone"],
        # Изображение
        "images": images,
    }


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

            defaults = extract_product_defaults(product_data)

            MoyskladProduct.objects.update_or_create(id=product_data["id"], defaults=defaults)
            success_count += 1

        except Exception as e:
            error_count += 1
            print(f"Ошибка обработки товара {product_data.get('id')}: {str(e)}")
            continue

    print(f"\nСинхронизация завершена. Успешно: {success_count}, Ошибок: {error_count}")
    return error_count == 0
