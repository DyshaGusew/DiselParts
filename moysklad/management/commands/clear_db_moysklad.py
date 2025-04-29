from django.core.management.base import BaseCommand
from moysklad.services import clear_db_moysklad


class Command(BaseCommand):
    help = "Очистка БД с товароми из мойсклад"

    def handle(self, *args, **options):
        if clear_db_moysklad():
            self.stdout.write(self.style.SUCCESS("✅ Удаленеи успешно"))
        else:
            self.stdout.write(self.style.ERROR("❌ Ошибка при удалении"))
