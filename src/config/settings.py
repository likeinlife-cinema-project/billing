from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from split_settings.tools import include

from misc.pydantic_yaml import YamlSettings


class Settings(YamlSettings):
    name: str
    allowed_hosts: list[str]
    logging_level: str = Field("INFO")


class SecretSettings(BaseSettings):
    debug: bool = Field(False)
    secret_key: str
    yaml_path: Path

    model_config = SettingsConfigDict(env_file="../.env", env_prefix="DJANGO_ADMIN_BILLING_")


secret_settings = SecretSettings()
yaml_settings = Settings.from_yaml(yaml_path=secret_settings.yaml_path)

LOCALE_PATHS = ["billing/locale"]

SECRET_KEY = secret_settings.secret_key

DEBUG = secret_settings.debug

ALLOWED_HOSTS = yaml_settings.allowed_hosts

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING_LEVEL = yaml_settings.logging_level

INTERNAL_IPS = [
    "127.0.0.1",
]

WSGI_APPLICATION = "config.wsgi.application"
AUTH_USER_MODEL = "user.User"

AUTHENTICATION_BACKENDS = [
    "jwt.backend.JWTAuthBackend",
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
