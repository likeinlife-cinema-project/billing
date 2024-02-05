from dependency_injector import containers, providers

from notifications.config import AuthSettings, NotificationSettings, BillingSettings
from notifications.notificator import Notificator


class Container(containers.DeclarativeContainer):
    settings_auth: providers.Singleton[AuthSettings] = providers.Singleton(AuthSettings)
    settings_notification: providers.Singleton[NotificationSettings] = providers.Singleton(NotificationSettings)
    settings_billing: providers.Singleton[BillingSettings] = providers.Singleton(BillingSettings)
    notificator: providers.Singleton[Notificator] = providers.Singleton(
        Notificator,
        settings_auth().login_url,
        settings_auth().user_info_url,
        settings_notification().notification_api_url,
        settings_billing().email,
        settings_billing().password,
    )
