from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_prefix="AUTH_")

    rsa_public_path: Path
    login_url: str

    @property
    def public_key(self):
        with open(self.rsa_public_path, "r") as pub_obj:
            return pub_obj.read()


auth_settings = AuthSettings()
