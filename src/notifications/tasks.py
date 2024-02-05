from datetime import timedelta

import structlog

from dependency_injector.wiring import Provide, inject
from django.utils import timezone

from config.celery import app
from notifications.containers import Container
from notifications.notificator import AbstractNotificator
from subscriptions.models import UserSubscription


logger = structlog.get_logger()


def get_almost_expired_subsciptions() -> list[UserSubscription] | None:
    return (
        UserSubscription.objects.filter(expire_at__date=(timezone.now() + timedelta(days=1)).date())
        .filter(prolong=True)
        .filter(archived=False)
        .select_related()
    )


@inject
def send_notification(
    user_id: str,
    type_: str,
    template: str,
    subject: str,
    params: dict,
    notificator: AbstractNotificator = Provide[Container.notificator],
):
    notificator.send_notification_request(
        type_=type_,
        template=template,
        subject=subject,
        user_id=user_id,
        params=params,
    )


@app.task
def send_notification_async(user_id: str, type_: str, template: str, subject: str, params: dict) -> None:
    send_notification(user_id, type_, template, subject, params)


@app.task
def remind() -> None:
    logger.info("Start reminder")
    user_subscriptions = get_almost_expired_subsciptions()

    for user_subscription in user_subscriptions:
        logger.info("sub:", user_subscription=user_subscription)
        send_notification_async.apply_async(
            args=(
                str(user_subscription.user_id),
                "email",
                "Payment-reminder",
                "Списание за продление подписки",
                {"subscription_name": user_subscription.subscription.name},
            )
        )

    logger.info("Finish reminder")
