from django.core.management.base import BaseCommand
from moysklad.services import clear_db_products


class Command(BaseCommand):
    help = "Очистка БД с продуктами на продажу"

    def handle(self, *args, **options):
        if clear_db_products():
            self.stdout.write(self.style.SUCCESS("✅ Удаленеи успешно"))
        else:
            self.stdout.write(self.style.ERROR("❌ Ошибка при удалении"))
