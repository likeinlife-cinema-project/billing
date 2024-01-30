from django.apps import AppConfig

from .containers import Container


class PaymentProlongationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payment_prolongation"

    def ready(self) -> None:
        container = Container()
        container.init_resources()
        container.wire(modules=["payment_prolongation.tasks"])
        return super().ready()
