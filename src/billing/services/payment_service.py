import json

from uuid import UUID

import structlog

from requests.exceptions import RequestException
from yookassa import Configuration, Payment, Refund
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from yookassa.domain.common import SecurityHelper
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder
from yookassa.domain.request.refund_request_builder import RefundRequestBuilder

from billing.config import settings
from billing.exceptions import UntrustedIpException, WrongEventException, PaymentGatewayException
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
        payment_method_id: str | None = None,
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
        payment_request = builder.build()
        idempotency_key = f"{str(user_id)}:{str(user_purchase_item_id)}"
        try:
            external_response = Payment.create(payment_request, idempotency_key)
        except RequestException:
            raise PaymentGatewayException(detail="Error in payment request")
        payment_out = PaymentOut(
            external_payment_id=external_response.id,
            refundable=external_response.refundable,
            status=external_response.status,
            confirmation=external_response.confirmation,
            user_id=user_id,
            user_purchase_item_id=user_purchase_item_id,
            amount=amount,
            currency=currency,
            recurrent=recurrent,
            payment_method_id=payment_method_id,
        )
        self.logger.info("Payment_out prepared", payment_out=payment_out)
        return payment_out

    def refund_payment(
        self,
        user_id: UUID,
        payment_id: UUID,
        external_payment_id: str,
        amount: float,
        currency: str,
        reason: str,
    ) -> RefundOut:
        builder = RefundRequestBuilder()
        builder.set_amount({"value": str(amount), "currency": currency}).set_payment_id(
            external_payment_id
        ).set_description(reason)
        refund_request = builder.build()
        try:
            external_response = Refund.create(refund_request, str(payment_id))
        except RequestException:
            raise PaymentGatewayException(detail="Error in refund request")
        refund_out = RefundOut(
            user_id=user_id,
            payment_id=payment_id,
            amount=amount,
            currency=currency,
            reason=reason,
            status=external_response.status,
            external_refund_id=external_response.id,
        )
        self.logger.info("Refund_out prepared", refund_out=refund_out)
        return refund_out

    def verify_incoming_ip(self, ip: str) -> None:
        if not SecurityHelper().is_ip_trusted(ip):
            raise UntrustedIpException()

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
