from dependency_injector import containers, providers

from billing.config import AuthSettings, BillingSettings, RedisSettings

from billing.mock.mock_payment_service import MockPaymentService
from billing.mock.mock_token_service import MockTokenService
from billing.mock.redis_db import get_redis
from billing.services.payment_service import PaymentService
from billing.services.token_service import TokenService


class Container(containers.DeclarativeContainer):
    settings: providers.Singleton[BillingSettings] = providers.Singleton(BillingSettings)
    if settings().mock_payment:
        settings_mock: providers.Singleton[RedisSettings] = providers.Singleton(RedisSettings)
        redis_conn = providers.Resource(get_redis, settings_mock().redis_host, settings_mock().redis_port)
        payment_service: providers.Singleton[MockPaymentService] = providers.Singleton(
            MockPaymentService, redis_conn, settings().redirect_url
        )
        token_service: providers.Singleton[MockTokenService] = providers.Singleton(MockTokenService, "")
    else:
        settings_auth: providers.Singleton[AuthSettings] = providers.Singleton(AuthSettings)
        payment_service = providers.Singleton(PaymentService, settings().redirect_url)
        token_service: providers.Singleton[TokenService] = providers.Singleton(TokenService, settings_auth().public_key)
