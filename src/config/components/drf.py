REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Billing service",
    "DESCRIPTION": "Service to manage payments and subscriptions",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
