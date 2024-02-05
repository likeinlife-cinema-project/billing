from django.apps import AppConfig

from notifications.containers import Container


class NotificationSenderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"

    def ready(self) -> None:
        container = Container()
        container.init_resources()
        container.wire(modules=["notifications.tasks"])
        return super().ready()
