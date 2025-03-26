from django.core.management.base import BaseCommand
from moysklad.services import sync_with_moysklad


class Command(BaseCommand):
    help = "Sync products with Moysklad"

    def handle(self, *args, **options):
        if sync_with_moysklad():
            self.stdout.write("✅ Sync successful")
        else:
            self.stdout.write("❌ Sync failed")
