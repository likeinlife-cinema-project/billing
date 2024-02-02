import uuid

import structlog
from dependency_injector.wiring import Provide, inject
from django.utils import timezone
from rest_framework.exceptions import ParseError, PermissionDenied

from billing.models import Payments
from billing.schemas.payment import PaymentOut
from billing.services import payment_service
from config.celery import app
from subscriptions.models import UserSubscription

from .containers import Container

logger = structlog.get_logger()


def get_last_payment(user_id: uuid.UUID, subscription_id: uuid.UUID) -> Payments | None:
    return (
        Payments.objects.filter(user_id=user_id)
        .filter(user_purchase_item_id=subscription_id)
        .order_by("created_at")
        .last()
    )


@inject
def make_new_payment(
    user_subscription: UserSubscription,
    payment_service: payment_service.PaymentService = Provide[Container.payment_service],
) -> PaymentOut | None:
    last_payment = get_last_payment(user_subscription.user_id, user_subscription.subscription.id)
    if not last_payment:
        logger.warning("Found subscription, not found payment", user_subscription_id=user_subscription.id)
        return
    try:
        new_payment = payment_service.request_payment(
            user_id=last_payment.user_id,
            recurrent=last_payment.recurrent,
            user_purchase_item_id=last_payment.user_purchase_item_id,
            amount=user_subscription.subscription.amount,
            currency=last_payment.currency,
            payment_method_id=last_payment.payment_method_id,
        )
        db_obj = Payments.objects.create(**new_payment.model_dump(exclude=["confirmation"]))
        logger.info("Make new payment", payment_id=db_obj.id)
        return new_payment
    except (ParseError, PermissionDenied) as exc:
        logger.error(exc, exc_info=True)
        return


def archive_user_subscription(
    user_subscription: UserSubscription,
) -> None:
    user_subscription.archived = True
    user_subscription.save()
    logger.info("Archive user_subscription", user_subscription_id=user_subscription.id)


@app.task
def start_prolongation() -> None:
    logger.info("Start prolongation")
    expired_user_subscriptions = (
        UserSubscription.objects.filter(expire_at__lt=timezone.now())
        .filter(prolong=True)
        .filter(archived=False)
        .select_related()
    )

    for user_subscription in expired_user_subscriptions:
        new_payment = make_new_payment(user_subscription)
        if not new_payment:
            continue
        archive_user_subscription(user_subscription)

    logger.info("Finish prolongation")
