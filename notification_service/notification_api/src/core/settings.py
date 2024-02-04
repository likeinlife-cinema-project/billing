from logging import config as logging_config
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger_setup import get_logging_settings


class PostgresSettings(BaseSettings):
    host: str = Field()
    port: str = Field()
    user: str = Field()
    password: str = Field()
    db_name: str = Field()

    model_config = SettingsConfigDict(env_prefix="api_postgres_", env_file=".env")


class PostgresTable(BaseSettings):
    schema_: str = Field("public")
    template: str = Field("template")
    notification_status: str = Field("notification_status")

    model_config = SettingsConfigDict(env_prefix="api_postgres_table_", env_file=".env")

    def get_table_name(self, name: str) -> str:
        return f"{self.schema_}.{name}"


class RabbitSettings(BaseSettings):
    queue_name: str = Field()
    host: str = Field()
    port: str = Field()
    user: str = Field()
    password: str = Field()

    model_config = SettingsConfigDict(env_prefix="api_rabbit_", env_file=".env")


class Settings(BaseSettings):
    project_root_url: str = Field("")
    postgres: ClassVar = PostgresSettings()
    postgres_table: ClassVar = PostgresTable()
    rabbit: ClassVar = RabbitSettings()
    rabbit_dsn: str = f"amqp://{rabbit.user}:{rabbit.password}@{rabbit.host}:{rabbit.port}/"
    postgres_dsn: str = (
        f"postgresql://{postgres.user}:{postgres.password}@{postgres.host}:{postgres.port}/{postgres.db_name}"
    )
    logging_level: str = Field("INFO")
    debug: bool = Field(False)

    model_config = SettingsConfigDict(env_prefix="notify_", env_file=".env")


settings = Settings()

logging_config.dictConfig(
    get_logging_settings(
        settings.logging_level,
        settings.debug,
    ),
)
