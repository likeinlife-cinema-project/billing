import os

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

LOCALE_PATHS = ["notifications/locale"]

SECRET_KEY = os.environ["DJANGO_ADMIN_NF_SECRET_KEY"]

DEBUG = os.environ.get("DJANGO_ADMIN_NF_DEBUG", "False") == "True"

LOGGING_LEVEL = os.environ.get("DJANGO_ADMIN_NF_LOGGING_LEVEL") or "INFO"

ALLOWED_HOSTS = os.environ["DJANGO_ADMIN_NF_ALLOWED_HOSTS"].split(",")

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    "127.0.0.1",
]

AUTH_USER_MODEL = "user.User"

AUTHENTICATION_BACKENDS = [
    "jwt.backend.JWTAuthBackend",
]

NOTIFICATION_API_URL = os.environ["DJANGO_ADMIN_NF_NOTIFICATION_API_URL"]

include(
    "components/apps.py",
    "components/database.py",
    "components/auth_password_validators.py",
    "components/folders.py",
    "components/celery.py",
    "components/templates.py",
    "components/middlewares.py",
    "components/logging.py",
)
