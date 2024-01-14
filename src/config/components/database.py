import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PG_ADMIN_BILLING_DB_NAME"),
        "USER": os.environ.get("PG_ADMIN_BILLING_USER"),
        "PASSWORD": os.environ.get("PG_ADMIN_BILLING_PASSWORD"),
        "HOST": os.environ.get("PG_ADMIN_BILLING_DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("PG_ADMIN_BILLING_DB_PORT", 5432),
        "OPTIONS": {
            "options": "-c search_path=public",
        },
    },
}
