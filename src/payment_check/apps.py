from django.apps import AppConfig

from .containers import Container


class PaymentCheckConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payment_check"

    def ready(self) -> None:
        container = Container()
        container.init_resources()
        container.wire(modules=["payment_check.tasks"])
        return super().ready()
