from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from billing.containers import Container


class BillingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "billing"
    verbose_name = _("billing")

    def ready(self) -> None:
        container = Container()
        container.init_resources()
        container.wire(modules=["billing.views"])
        return super().ready()
