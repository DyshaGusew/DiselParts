from .base import *

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]

# SQLite для разработки
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
