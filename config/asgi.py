import os
from dotenv import load_dotenv

load_dotenv()
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.local"))

application = get_asgi_application()
