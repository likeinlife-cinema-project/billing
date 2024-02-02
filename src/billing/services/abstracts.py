from abc import ABC, abstractmethod
from uuid import UUID

from billing.schemas.notification import Notification
from billing.schemas.payment import PaymentOut
from billing.schemas.refund import RefundOut


class AbstractPaymentService(ABC):
    redirect_url: str
    logger: str

    @abstractmethod
    def request_payment(
        self,
        user_id: UUID,
        recurrent: bool,
        user_purchase_item_id: UUID,
        amount: float,
        currency: str,
        payment_method_id: str | None = None,
    ) -> PaymentOut:
        pass

    @abstractmethod
    def refund_payment(
        self,
        user_id: UUID,
        payment_id: UUID,
        external_payment_id: str,
        amount: float,
        currency: str,
        reason: str,
    ) -> RefundOut:
        pass

    @abstractmethod
    def verify_incoming_ip(self, ip: str) -> None:
        pass

    @abstractmethod
    def process_notification(self, data: dict) -> Notification:
        pass

    @abstractmethod
    def get_payment_info(self, payment_id: str) -> dict:
        pass

    @abstractmethod
    def get_refund_info(self, refund_id: str) -> dict:
        pass


class AbstractTokenService(ABC):
    public_key: str
    logger: str

    @abstractmethod
    def get_user_id_from_token(self, access_token: str) -> str:
        pass
