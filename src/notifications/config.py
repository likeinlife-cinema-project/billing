from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_prefix="AUTH_")

    login_url: str
    user_info_url: str


class NotificationSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_prefix="DJANGO_ADMIN_NF_")

    notification_api_url: str


class BillingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_prefix="BILLING_")

    email: str
    password: str


settings_auth = AuthSettings()
settings_notification = NotificationSettings()
settings_billing = BillingSettings()
