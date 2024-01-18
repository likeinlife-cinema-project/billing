import logging

from django.contrib import admin

from notifications.models import Notification, NotificationStatus, Template

logger = logging.getLogger(__name__)


@admin.register(Notification)
class RegularNotificationAdmin(admin.ModelAdmin):
    list_display = ("subject", "start_at", "status", "type", "roles", "template", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("subject",)
    readonly_fields = ("status",)


@admin.register(NotificationStatus)
class NotificationStatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "task_id",
        "subject",
        "status",
        "notification_type",
        "description",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("subject", "task_id", "id")
    readonly_fields = ("status", "notification_type", "subject")


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("slug", "content", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("slug",)
