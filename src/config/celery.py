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
    "prolongation": {"task": "payment_prolongation.tasks.start_prolongation", "schedule": crontab()},
    "check_need_confirm": {"task": "payment_check.tasks.start_check_need_confirm", "schedule": crontab()},
    "check_pending": {"task": "payment_check.tasks.start_check_pending", "schedule": crontab(minute="*/10")},
}


@setup_logging.connect
def setup_logging(*args, **kwargs) -> None:
    dictConfig(LOGGING)
