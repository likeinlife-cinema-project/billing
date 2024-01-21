from abc import ABC, abstractmethod


class AbstractPaymentService(ABC):
    @abstractmethod
    def get_payment_link(self, data: dict) -> str:
        pass

    @abstractmethod
    def request_payment(self, data: dict) -> dict:
        pass

    @abstractmethod
    def refund_payment(self, data: dict) -> dict:
        pass

    @abstractmethod
    def process_notification(self):
        pass
