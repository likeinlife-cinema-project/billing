import os

RABBIT_HOST = os.environ.get("APP_RABBIT_HOST", "127.0.0.1")
RABBIT_PORT = os.environ.get("APP_RABBIT_PORT", 5672)
RABBIT_USER = os.environ.get("APP_RABBIT_USER", "guest")
RABBIT_PASSWORD = os.environ.get("APP_RABBIT_PASSWORD", "guest")

REDIS_HOST = os.environ.get("APP_REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("APP_REDIS_PORT", 6379)

CELERY_BROKER_URL = f"amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}"
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_IMPORTS = ("billing.tasks", "payment_prolongation.tasks", "payment_check.tasks", "notifications.tasks")
