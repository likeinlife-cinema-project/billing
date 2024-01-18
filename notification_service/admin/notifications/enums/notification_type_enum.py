from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationTypeEnum(models.TextChoices):
    EMAIL = "EMAIL", _("Email")
    WEBSOCKET = "WEBSOCKET", _("Websocket")
    PUSH = "PUSH", _("Push")
    TEST = "TEST", _("TEST")
