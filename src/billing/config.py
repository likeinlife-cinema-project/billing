from pydantic_settings import BaseSettings, SettingsConfigDict


class BillingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="BILLING_")

    shop_id: int
    secret_key: str
    redirect_url: str


settings = BillingSettings()
