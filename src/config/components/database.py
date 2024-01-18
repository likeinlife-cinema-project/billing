from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    db_name: str
    user: str
    password: str
    host: str
    port: int = Field(5432)

    model_config = SettingsConfigDict(env_file=".env", env_prefix="PG_ADMIN_BILLING_")


postgres = PostgresSettings()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": postgres.db_name,
        "USER": postgres.user,
        "PASSWORD": postgres.password,
        "HOST": postgres.host,
        "PORT": postgres.port,
        "OPTIONS": {
            "options": "-c search_path=public",
        },
    },
}
