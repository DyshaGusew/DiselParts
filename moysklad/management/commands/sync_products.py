from django.core.management.base import BaseCommand
from moysklad.services import sync_products_with_moysklad


class Command(BaseCommand):
    help = "Синхронизация товаров с МойСклад"

    def handle(self, *args, **options):
        if sync_products_with_moysklad():
            self.stdout.write(self.style.SUCCESS("✅ Синхронизация успешна"))
        else:
            self.stdout.write(self.style.ERROR("❌ Синхронизация завершена с ошибками"))
