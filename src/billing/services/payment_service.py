import json

from uuid import UUID

import structlog

from rest_framework import status
from rest_framework.exceptions import ParseError, PermissionDenied, AuthenticationFailed
from requests.exceptions import HTTPError
from yookassa import Configuration, Payment, Refund
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from yookassa.domain.common import SecurityHelper
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder
from yookassa.domain.request.refund_request_builder import RefundRequestBuilder

from billing.config import settings
from billing.exceptions import WrongEventException
from billing.services.abstracts import AbstractPaymentService
from billing.schemas.notification import Notification
from billing.schemas.payment import PaymentOut
from billing.schemas.refund import RefundOut


class PaymentService(AbstractPaymentService):
    def __init__(self, redirect_url: str) -> None:
        self.configuration = Configuration.configure(settings.shop_id, settings.secret_key)
        self.logger = structlog.get_logger(__name__)
        self.redirect_url = redirect_url

    def request_payment(
        self,
        user_id: UUID,
        recurrent: bool,
        user_purchase_item_id: UUID,
        amount: float,
        currency: str,
        payment_method_id: str,
    ) -> PaymentOut:
        builder = PaymentRequestBuilder()
        if payment_method_id:
            builder.set_amount({"value": str(amount), "currency": currency}).set_capture(True).set_payment_method_id(
                payment_method_id
            )
        else:
            builder.set_amount({"value": str(amount), "currency": currency}).set_confirmation(
                {"type": ConfirmationType.REDIRECT, "return_url": self.redirect_url}
            ).set_capture(True).set_save_payment_method(recurrent)
        try:
            payment_request = builder.build()
            idempotency_key = f"{str(user_id)}:{str(user_purchase_item_id)}"
            external_response = Payment.create(payment_request, idempotency_key)
            payment_out = PaymentOut(
                external_payment_id=external_response.id,
                refundable=external_response.refundable,
                status=external_response.status,
                confirmation=external_response.confirmation,
                user_id=user_id,
                user_purchase_item_id=user_purchase_item_id,
                amount=amount,
                currency=currency,
                payment_method_id=payment_method_id,
                recurrent=recurrent,
            )
            self.logger.info(f"{payment_out=}")
            return payment_out
        except ValueError as err:
            self.logger.error(f"{err=}")
            raise ParseError(detail="Wrong data sent to payment builder", code=status.HTTP_400_BAD_REQUEST)
        except HTTPError as err:
            self.logger.error(f"{err=}")
            raise PermissionDenied(detail="Can't reach payment operator for payment", code=status.HTTP_403_FORBIDDEN)

    def refund_payment(
        self, user_id: UUID, payment_id: UUID, external_payment_id: str, amount: float, currency: str, reason: str
    ) -> RefundOut:
        builder = RefundRequestBuilder()
        builder.set_amount({"value": str(amount), "currency": currency}).set_payment_id(
            external_payment_id
        ).set_description(reason)
        try:
            refund_request = builder.build()
        except ValueError as err:
            self.logger.error(f"{err=}")
            raise ParseError(detail="Wrong data sent to refund builder", code=status.HTTP_400_BAD_REQUEST)
        try:
            external_response = Refund.create(refund_request, str(payment_id))
            refund_out = RefundOut(
                user_id=user_id,
                payment_id=payment_id,
                amount=amount,
                currency=currency,
                reason=reason,
                status=external_response.status,
                external_refund_id=external_response.id,
            )
            self.logger.info(f"{refund_out=}")
            return refund_out
        except HTTPError as err:
            self.logger.error(f"{err=}")
            raise PermissionDenied(detail="Can't reach payment operator for refund", code=status.HTTP_403_FORBIDDEN)

    def verify_incoming_ip(self, ip: str) -> None:
        if not SecurityHelper().is_ip_trusted(ip):
            raise AuthenticationFailed(detail="Wrong incoming IP in notification", code=status.HTTP_400_BAD_REQUEST)

    def process_notification(self, data: dict) -> Notification:
        notification_object = WebhookNotificationFactory().create(data)
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            payment_response: dict = json.loads(notification_object.object.json())
            notification = Notification(
                id=notification_object.object.id,
                type="payment",
                payment_method_type=payment_response.get("payment_method")["type"],
                payment_method_id=payment_response.get("payment_method")["id"],
                refundable=payment_response.get("refundable"),
            )
            return notification
        elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
            notification = Notification(id=notification_object.object.id, type="refund")
            return notification
        raise WrongEventException()

    def get_payment_info(self, payment_id: str) -> dict:
        res = Payment.find_one(payment_id)
        res_ = json.loads(res.json())
        return res_

    def get_refund_info(self, refund_id: str) -> dict:
        res = Refund.find_one(refund_id)
        res_ = json.loads(res.json())
        return res_
