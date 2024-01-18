from pathlib import Path
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class UserDBSettings(BaseSettings):
    host: str
    port: str = Field("5432")
    user: str
    db_name: str
    password: str

    model_config = SettingsConfigDict(env_prefix="notify_user_db_", env_file=".env")


class NotifyDBSettings(BaseSettings):
    host: str
    port: str = Field("5432")
    user: str
    db_name: str
    password: str

    notify_status_table_name: str = Field("notification_status")

    model_config = SettingsConfigDict(env_prefix="notify_notify_db_", env_file=".env")


class RabbitSettings(BaseSettings):
    host: str
    port: str = Field("5672")
    user: str = Field("guest")
    password: str = Field("guest")

    model_config = SettingsConfigDict(env_prefix="notify_rabbit_", env_file=".env")


class SMTPSettings(BaseSettings):
    login: str
    password: str
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix="notify_smtp_", env_file=".env")


class QueueNameSettings(BaseSettings):
    user_provided: str
    notify_task: str
    dead_letter: str
    dead_letter_ttl: int = Field(5000)
    dead_letter_max_count: int = Field(5)

    model_config = SettingsConfigDict(env_prefix="notify_queue_", env_file=".env")


class AuthSettings(BaseSettings):
    password: str
    email: str
    host: str
    port: str
    sign_in_route: str

    model_config = SettingsConfigDict(env_prefix="notify_auth_", env_file=".env")

    def get_base_url(self) -> str:
        return f"http://{self.host}:{self.port}/api/v1"


class Settings(BaseSettings):
    user_db: ClassVar = UserDBSettings()
    notify_db: ClassVar = NotifyDBSettings()
    rabbit: ClassVar = RabbitSettings()
    smtp: ClassVar = SMTPSettings()
    queue: ClassVar = QueueNameSettings()
    auth: ClassVar = AuthSettings()

    rabbit_url: str = f"amqp://{rabbit.user}:{rabbit.password}@{rabbit.host}:{rabbit.port}/"
    user_db_dsn: str = f"postgres://{user_db.user}:{user_db.password}@{user_db.host}:{user_db.port}/{user_db.db_name}"
    notify_db_dsn: str = (
        f"postgres://{notify_db.user}:{notify_db.password}@{notify_db.host}:{notify_db.port}/{notify_db.db_name}"
    )

    console_logging_level: str = Field("DEBUG")
    json_logging_level: str = Field("ERROR")


settings = Settings()
PROJECT_ROOT = Path(__file__).parent.parent
