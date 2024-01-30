import os
from logging.config import dictConfig

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging

from .components.logging import LOGGING

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("billing")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "do_test_task": {"task": "billing.tasks.test_billing_task", "schedule": crontab()},
    "prolongation": {"task": "payment_prolongation.tasks.start_prolongation", "schedule": crontab()},
}


@setup_logging.connect
def setup_logging(*args, **kwargs) -> None:
    dictConfig(LOGGING)
