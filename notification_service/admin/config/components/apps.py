from django.conf import settings

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "django_structlog",
    # Local apps
    "notifications",
    "user",
    "jwt",
]

if settings.DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
