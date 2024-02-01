import structlog
from dependency_injector.wiring import Provide, inject
from django.utils import timezone
from requests.exceptions import RequestException

from billing.config import settings
from billing.models import Payments, Status
from billing.services import payment_service
from config.celery import app
from config.misc import get_timedelta_from_string
from subscriptions.models import UserSubscription, Subscription

from .containers import Container

logger = structlog.get_logger()


def get_processing_payments(status: Status) -> list[Payments]:
    return Payments.objects.filter(status=status).order_by("created_at")


@inject
def get_payment_status(
    payment: Payments,
    payment_service: payment_service.PaymentService = Provide[Container.payment_service],
) -> str:
    payment_info = payment_service.get_payment_info(payment.external_payment_id)
    logger.info("Got payment info", payment_info=payment_info)
    return payment_info["status"]


def add_user_subscription(
    payment: Payments,
) -> None:
    subscription = Subscription.objects.get(id=payment.user_purchase_item_id)
    user_subscription = UserSubscription.objects.create(
        user_id=payment.user_id,
        subscription=Subscription(id=payment.user_purchase_item_id),
        expire_at=timezone.now() + get_timedelta_from_string(subscription.period),
        prolong=payment.recurrent,
    )
    user_subscription.save()
    logger.info("Add user_subscription", user_subscription_id=user_subscription.id)


def process_payments(payments: list[Payments]) -> None:
    logger.debug("Got payment list", processing_payments=payments)
    for payment in payments:
        try:
            status = get_payment_status(payment)
            logger.info("Get payment status", payment_id=payment.id, status=status)
            if status == "succeeded":
                payment.status = Status.succeeded
                add_user_subscription(payment)
            else:
                if (timezone.now() - payment.created_at).seconds > settings.payment_expiration_secs:
                    payment.status = Status.canceled
                    logger.warning("Payment was canceled due timeout", payment_id=payment.id)
            payment.save()
        except RequestException as err:
            logger.error("Cant get payment status", payment_id=payment.id, error=err)
        except Exception as err:
            logger.error("Unexpected error", payment_id=payment.id, error=err)


@app.task
def start_check_need_confirm() -> None:
    logger.info("Start check 'need confirm' payments")
    payment_list = get_processing_payments(status=Status.need_confirm)
    process_payments(payment_list)
    logger.info("Finish check")


@app.task
def start_check_pending() -> None:
    logger.info("Start check 'pending' payments")
    payment_list = get_processing_payments(status=Status.pending)
    process_payments(payment_list)
    logger.info("Finish check")
