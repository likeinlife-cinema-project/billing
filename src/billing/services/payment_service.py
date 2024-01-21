import json

from typing import Optional

import structlog

from rest_framework import status
from rest_framework.exceptions import ParseError, PermissionDenied, AuthenticationFailed
from rest_framework.request import Request
from requests.exceptions import HTTPError
from yookassa import Configuration, Payment, Refund
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from yookassa.domain.common import SecurityHelper
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder
from yookassa.domain.request.refund_request_builder import RefundRequestBuilder

from billing.services.abstracts import AbstractPaymentService
from billing.config import settings


class PaymentService(AbstractPaymentService):
    def __init__(self) -> None:
        self.configuration = Configuration.configure(settings.shop_id, settings.secret_key)
        self.logger = structlog.get_logger()

    def get_payment_link(self, data: dict) -> Optional[tuple[str, dict]]:
        modified_data = self.request_payment(data, False)
        if modified_data.get("confirmation"):
            link = modified_data.get("confirmation")["confirmation_url"]
            self.logger.info(f"{link=}")
            return link, data

    def request_payment(self, data: dict, repeated: bool) -> dict:
        builder = PaymentRequestBuilder()
        if repeated:
            builder.set_amount({"value": data.get("amount"), "currency": data.get("currency")}).set_capture(
                True
            ).set_payment_method_id(data.get("payment_method_id"))
        else:
            builder.set_amount({"value": data.get("amount"), "currency": data.get("currency")}).set_confirmation(
                {"type": ConfirmationType.REDIRECT, "return_url": settings.redirect_url}
            ).set_capture(True).set_save_payment_method(data.get("recurrent"))
        try:
            payment_request = builder.build()
            external_response = Payment.create(payment_request, data.get("user_purchase_item_id"))
            accepted_data: dict = json.loads(external_response.json())
            data["external_payment_id"] = accepted_data.get("id")
            data["refundable"] = accepted_data.get("refundable")
            data["status"] = accepted_data.get("status")
            data["confirmation"] = accepted_data.get("confirmation")
            self.logger.info(f"enriched {data=}")
            return data
        except ValueError as err:
            self.logger.error(f"{err=}")
            raise ParseError(detail="Wrong data sent to payment builder", code=status.HTTP_400_BAD_REQUEST)
        except HTTPError as err:
            self.logger.error(f"{err=}")
            raise PermissionDenied(detail="Can't reach payment operator for payment", code=status.HTTP_403_FORBIDDEN)

    def refund_payment(self, data: dict) -> dict:
        builder = RefundRequestBuilder()
        builder.set_amount({"value": data.get("amount"), "currency": data.get("currency")}).set_payment_id(
            data.get("external_payment_id")
        ).set_description(data.get("reason"))
        try:
            refund_request = builder.build()
            external_response = Refund.create(refund_request, data.get("payment_id"))
            accepted_data: dict = json.loads(external_response.json())
            data["status"] = accepted_data.get("status")
            data["external_refund_id"] = accepted_data.get("id")
            return data
        except ValueError as err:
            self.logger.error(f"{err=}")
            raise ParseError(detail="Wrong data sent to refund builder", code=status.HTTP_400_BAD_REQUEST)
        except HTTPError as err:
            self.logger.error(f"{err=}")
            raise PermissionDenied(detail="Can't reach payment operator for refund", code=status.HTTP_403_FORBIDDEN)

    def verify_incoming_ip(self, request: Request):
        ip = request._request.headers.get("X-Forwarded-For")
        if not SecurityHelper().is_ip_trusted(ip):
            raise AuthenticationFailed(detail="Wrong incoming IP in notification", code=status.HTTP_400_BAD_REQUEST)

    def process_notification(self, data: dict):
        notification_object = WebhookNotificationFactory().create(data)
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            # TODO: кладем в очередь либо external_id + type, либо data + type
            pass
        elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
            # TODO: кладем в очередь либо external_id + type, либо data + type
            pass
        else:
            raise ParseError(detail="Unexpected notification type", code=status.HTTP_400_BAD_REQUEST)


def get_payment_service() -> PaymentService:
    return PaymentService()
