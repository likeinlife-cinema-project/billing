from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class NotificationRegistrationStatus(TextChoices):
    WAITING = "WAITING", _("WAITING")
    FAILED = "FAILED", _("FAILED")
    DONE = "DONE", _("DONE")
