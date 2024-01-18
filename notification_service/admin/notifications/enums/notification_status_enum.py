from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationStatusEnum(models.TextChoices):
    PENDING = "PG", _("Pending")
    OK = "OK", _("Ok")
    ERROR = "ER", _("Error")
