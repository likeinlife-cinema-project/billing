from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_prefix="AUTH_", secrets_dir="/run/secrets")

    login_url: str
    rsa_pub: str


auth_settings = AuthSettings()
