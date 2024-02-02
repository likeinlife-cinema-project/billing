from uuid import UUID

from django.db import transaction
from django.contrib import messages
from datetime import datetime
import structlog
from dependency_injector.wiring import Provide
from django.contrib import admin  # noqa

from billing.containers import Container
from billing.models import Payments, Refunds, Status
from billing.services.abstracts import AbstractPaymentService
from subscriptions.models import UserSubscription

logger = structlog.get_logger(__name__)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "external_payment_id",
        "payment_method",
        "amount",
        "currency",
        "status",
        "refundable",
        "recurrent",
    )
    list_display_links = ("user_id", "external_payment_id")
    ordering = ["created_at"]
    search_fields = ["user_id", "external_payment_id"]
    list_per_page = 30


@admin.register(Refunds)
class RefundsAdmin(admin.ModelAdmin):
    list_display = ("user_id", "external_refund_id", "amount", "currency", "status", "reason")
    list_display_links = ("user_id", "external_refund_id")
    ordering = ["created_at"]
    search_fields = ["user_id", "external_refund_id"]
    list_per_page = 30
    actions = ["accept_refund", "reject_refund"]

    @admin.action(description="Accept refund")
    def accept_refund(
        self,
        request,
        queryset,
        service: AbstractPaymentService = Provide[Container.payment_service],
    ):
        for refund in queryset:
            if refund.status != Status.need_confirm:
                logger.info(f"Refund {refund} is not allowed to refund because of status {Status.need_confirm}.")
                self.message_user(
                    request,
                    f"Refund {refund} is not allowed to refund because of status {Status.need_confirm}.",
                    level=messages.ERROR,
                )
                continue
            try:
                amount = self.__calculate_amount(refund.payment.id, refund.user_subscription_id)
                if not amount:
                    self.message_user(
                        request,
                        f"Failed to calculate amount to refund for Refund {refund}",
                        level=messages.ERROR,
                    )
                    continue
                service_refund = service.refund_payment(
                    user_id=refund.user_id,
                    payment_id=refund.payment.id,
                    external_payment_id=refund.payment.external_payment_id,
                    amount=amount,
                    currency=refund.payment.currency,
                    reason=refund.reason,
                )
                if service_refund:
                    with transaction.atomic():
                        refund.status = Status.succeeded
                        refund.save()

                        user_subscription = UserSubscription.objects.get(id=refund.user_subscription_id)
                        user_subscription.prolong = False
                        user_subscription.archived = True
                        user_subscription.save()
                else:
                    self.message_user(
                        request,
                        f"Some problems occurred with service to refund {refund}",
                        level=messages.ERROR,
                    )
            except Exception as ex:
                logger.error(ex)
                self.message_user(
                    request,
                    f"Some problems occurred with service to refund {refund}",
                    level=messages.ERROR,
                )

    def __calculate_amount(self, payment_id: UUID, user_subscription_id: UUID) -> float | None:
        from billing.models import Payments
        from subscriptions.models import UserSubscription, SubscriptionPeriods

        payment_amount = Payments.objects.get(pk=payment_id).amount
        user_subscription = UserSubscription.objects.get(id=user_subscription_id)
        if not user_subscription:
            return None
        if user_subscription.expire_at >= datetime.now():
            return None
        subscription_period = {
            SubscriptionPeriods.month: 30,
            SubscriptionPeriods.year: 365,
        }[user_subscription.subscription.period]
        return (user_subscription.expire_at - datetime.now()).days / subscription_period * payment_amount

    @admin.action(description="Reject refund")
    def reject_refund(self, request, queryset):
        queryset.filter(status=Status.need_confirm).update(status=Status.canceled)
