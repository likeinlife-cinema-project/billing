from django.db import models
from django.utils.translation import gettext_lazy as _

from models_mixins import TimeStampedMixin, UUIDMixin


class Currency(models.Choices):
    rub = "RUB"
    usd = "USD"
    eur = "EUR"


class Status(models.TextChoices):
    need_confirm = "need_confirm"
    succeeded = "succeeded"
    canceled = "canceled"
    pending = "pending"
    error = "error"


class Payments(UUIDMixin, TimeStampedMixin):
    user_id = models.UUIDField(_("user_id"), blank=False, null=False)
    user_purchase_item_id = models.UUIDField(_("user_purchase_item_id"), blank=False, null=False)
    external_payment_id = models.CharField(_("external_payment_id"), blank=False, null=False, unique=True)
    payment_method = models.CharField(_("payment_method"), blank=True)
    payment_method_id = models.CharField(_("payment_method_id"), blank=True)
    amount = models.FloatField(_("amount"), blank=False)
    currency = models.CharField(_("currency"), choices=Currency.choices, blank=False, null=False)
    status = models.CharField(_("status"), choices=Status.choices, blank=False, null=False, default=Status.pending)
    recurrent = models.BooleanField(_("recurrent"))
    refundable = models.BooleanField(_("refundable"))

    class Meta:
        db_table = 'public"."payments'
        verbose_name = _("payments")
        verbose_name_plural = _("payments")
        indexes = [
            models.Index(fields=["user_id", "user_purchase_item_id"], name="user_id_item_id_idx"),
            models.Index(fields=["external_payment_id"], name="external_payment_idx"),
        ]

    def __str__(self) -> str:
        return str(self.id)


class Refunds(UUIDMixin, TimeStampedMixin):
    user_id = models.UUIDField(_("user_id"), blank=False, null=False)
    payment = models.ForeignKey(Payments, on_delete=models.RESTRICT, blank=False, null=False)
    external_refund_id = models.CharField(_("external_refund_id"), unique=True)
    amount = models.FloatField(_("amount"), blank=False)
    currency = models.CharField(_("currency"), choices=Currency.choices, blank=False, null=False)
    status = models.CharField(_("status"), choices=Status.choices, blank=False, null=False, default=Status.pending)
    reason = models.TextField(_("reason"))

    class Meta:
        db_table = 'public"."refunds'
        verbose_name = _("refunds")
        verbose_name_plural = _("refunds")
        indexes = [
            models.Index(fields=["user_id", "payment"], name="user_id_payment_id_idx"),
            models.Index(fields=["external_refund_id"], name="external_refund_idx"),
        ]

    def __str__(self) -> str:
        return str(self.id)
