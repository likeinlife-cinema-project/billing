from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from split_settings.tools import include


class ProjectSettings(BaseSettings):
    name: str = Field("Django")
    secret_key: str
    allowed_hosts: list[str]
    debug: str = Field("False")
    logging_level: str = Field("INFO")

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DJANGO_ADMIN_BILLING_")


settings = ProjectSettings()


LOCALE_PATHS = ["billing/locale"]

SECRET_KEY = settings.secret_key

DEBUG = settings.debug

ALLOWED_HOSTS = settings.allowed_hosts

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING_LEVEL = settings.logging_level

INTERNAL_IPS = [
    "127.0.0.1",
]


include(
    "components/application_definition.py",
    "components/auth_password_validators.py",
    "components/folders.py",
    "components/database.py",
    "components/internationalization.py",
    "components/worker.py",
    "components/logging.py",
    "components/drf.py",
)
