from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BillingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_prefix="BILLING_")

    shop_id: int
    secret_key: str
    redirect_url: str
    mock_payment: bool = False


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_prefix="APP_")

    redis_host: str
    redis_port: int


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_prefix="AUTH_")

    rsa_public_path: Path = Field()

    @property
    def public_key(self):
        with open(self.rsa_public_path, "r") as pub_obj:
            return pub_obj.read()


settings = BillingSettings()
settings_mock = RedisSettings()
settings_auth = AuthSettings()
