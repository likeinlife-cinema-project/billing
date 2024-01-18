from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class PostgresSettings(BaseSettings):
    host: str = Field()
    port: str = Field()
    user: str = Field()
    password: str = Field()
    db_name: str = Field()

    model_config = SettingsConfigDict(env_prefix="api_postgres_", env_file=".env")


class Settings(BaseSettings):
    api_base_url: str = Field("http://api:8001")
    register_event_endpoint: str = Field("/api/v1/events/")
    postgres: ClassVar = PostgresSettings()


settings = Settings()
