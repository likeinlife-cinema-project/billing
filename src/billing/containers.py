from dependency_injector import containers, providers

from billing.services.payment_service import PaymentService


class Container(containers.DeclarativeContainer):
    payment_service = providers.Singleton(PaymentService)
