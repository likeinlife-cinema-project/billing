from django.conf import settings

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "config.components.exception_hander.custom_exception_handler",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Billing service",
    "DESCRIPTION": "Service to manage payments and subscriptions",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
}

if not settings.DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (("rest_framework.renderers.JSONRenderer",),)
