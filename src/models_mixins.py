import uuid

from django.db import models
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True, db_default=Now())
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True, db_default=Now())

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
