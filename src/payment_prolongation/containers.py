from dependency_injector import containers, providers

from billing.config import BillingSettings, RedisSettings
from billing.mock.mock_payment_service import MockPaymentService
from billing.mock.redis_db import get_redis
from billing.services.payment_service import PaymentService


class Container(containers.DeclarativeContainer):
    settings: providers.Singleton[BillingSettings] = providers.Singleton(BillingSettings)
    if settings().mock_payment:
        settings_mock: providers.Singleton[RedisSettings] = providers.Singleton(RedisSettings)
        redis_conn = providers.Resource(get_redis, settings_mock().redis_host, settings_mock().redis_port)
        payment_service: providers.Singleton[MockPaymentService] = providers.Singleton(
            MockPaymentService, redis_conn, settings().redirect_url
        )
    else:
        payment_service = providers.Singleton(PaymentService, settings().redirect_url)
