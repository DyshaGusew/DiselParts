from .base import *
import pymysql

pymysql.install_as_MySQLdb()

ALLOWED_HOSTS = ["diesel-parts-anapa.ru"]
CSRF_TRUSTED_ORIGINS = ["https://diesel-parts-anapa.ru.xsph.ru"]

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

STATIC_ROOT = BASE_DIR.parent / "public_html/static"
