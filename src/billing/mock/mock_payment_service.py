import json

from typing import Optional
from uuid import UUID, uuid4

import structlog
from redis import Redis

from billing.exceptions import WrongEventException
from billing.schemas.notification import Notification
from billing.schemas.payment import Confirmation, PaymentOut
from billing.schemas.refund import RefundOut
from billing.services.abstracts import AbstractPaymentService
from billing.tasks import mock_send_notification


class MockPaymentService(AbstractPaymentService):
    def __init__(self, redis: Redis, redirect_url: str) -> None:
        self.redis = redis
        self.logger = structlog.get_logger(__name__)
        self.redirect_url = redirect_url

    def request_payment(
        self, user_id: UUID, recurrent: bool, user_purchase_item_id: UUID, amount: float, currency: str
    ) -> PaymentOut:
        idempotency_key = f"{str(user_id)}:{str(user_purchase_item_id)}"
        redis_payment = self.check_payment_idempotency_key(idempotency_key)
        if redis_payment:
            payment_out = PaymentOut(
                external_payment_id=redis_payment.get("id"),
                refundable=redis_payment.get("refundable"),
                status=redis_payment.get("status"),
                user_id=user_id,
                user_purchase_item_id=user_purchase_item_id,
                amount=amount,
                currency=currency,
                recurrent=redis_payment.get("payment_method")["saves"],
            )
            return payment_out
        external_payment_id = str(uuid4())
        payment_out = PaymentOut(
            external_payment_id=external_payment_id,
            refundable=False,
            status="pending",
            user_id=user_id,
            user_purchase_item_id=user_purchase_item_id,
            amount=amount,
            currency=currency,
            recurrent=recurrent,
        )
        payment_method_id = str(uuid4())
        payment_object = {
            "id": external_payment_id,
            "status": "succeeded",
            "amount": {"value": str(amount), "currency": currency},
            "payment_method": {"type": "bank_card", "id": payment_method_id, "saves": recurrent},
            "refundable": True,
        }
        self.redis.set(name=external_payment_id, value=json.dumps(payment_object))
        self.redis.set(name=idempotency_key, value=external_payment_id, ex=60 * 60 * 24)
        confirmation = Confirmation(type="redirect", confirmation_url=self.redirect_url)
        payment_out.confirmation = confirmation
        self.logger.info(f"{payment_out=}")
        mock_send_notification.apply_async(args=(external_payment_id, "payment"), countdown=20)
        return payment_out

    def refund_payment(
        self, user_id: UUID, payment_id: UUID, external_payment_id: str, amount: float, currency: str, reason: str
    ) -> RefundOut:
        idempotency_key = str(payment_id)
        self.check_refund_idempotency_key(idempotency_key)
        external_refund_id = str(uuid4())
        refund_object = {
            "id": external_refund_id,
            "payment_id": external_payment_id,
            "status": "succeeded",
            "amount": {"value": amount, "currency": currency},
            "description": reason,
        }
        self.redis.set(name=external_refund_id, value=json.dumps(refund_object))
        self.redis.set(name=idempotency_key, value=external_refund_id, ex=60 * 60 * 24)
        refund_out = RefundOut(
            user_id=user_id,
            payment_id=payment_id,
            amount=amount,
            currency=currency,
            reason=reason,
            status="pending",
            external_refund_id=external_refund_id,
        )
        mock_send_notification.apply_async(args=(external_refund_id, "refund"), countdown=20)
        return refund_out

    def verify_incoming_ip(self, ip: str) -> None:
        pass

    def process_notification(self, data: dict) -> Notification:
        event = data.get("event")
        if event == "payment":
            payment_response: dict = data.get("object")
            notification = Notification(
                id=data.get("object")["id"],
                type="payment",
                payment_method_type=payment_response.get("payment_method")["type"],
                payment_method_id=payment_response.get("payment_method")["id"],
                refundable=payment_response.get("refundable"),
            )
            return notification
        elif event == "refund":
            notification = Notification(id=data.get("object")["id"], type="refund")
            return notification
        raise WrongEventException()

    def get_payment_info(self, payment_id: str) -> dict:
        payment_object = self.redis.get(name=payment_id)
        payment_object_ = json.loads(payment_object)
        return payment_object_

    def get_refund_info(self, refund_id: str) -> dict:
        refund_object = self.redis.get(name=refund_id)
        refund_object_ = json.loads(refund_object)
        return refund_object_

    def check_payment_idempotency_key(self, idempotency_key: str) -> Optional[dict]:
        in_redis = self.redis.get(idempotency_key)
        if in_redis:
            return self.get_payment_info(in_redis)

    def check_refund_idempotency_key(self, idempotency_key: str) -> Optional[dict]:
        in_redis = self.redis.get(idempotency_key)
        if in_redis:
            return self.get_refund_info(in_redis)
