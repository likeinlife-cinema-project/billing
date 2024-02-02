from django.apps import AppConfig

from .containers import AuthContainer


class JwtConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jwt"

    def ready(self) -> None:
        container = AuthContainer()
        container.init_resources()
        container.wire(modules=["jwt.backend"])
        return super().ready()
