from django.contrib import admin  # noqa

from billing.models import Payments, Refunds


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "external_payment_id",
        "payment_method",
        "amount",
        "currency",
        "status",
        "refundable",
        "recurrent",
    )
    list_display_links = ("user_id", "external_payment_id")
    ordering = ["created_at"]
    search_fields = ["user_id", "external_payment_id"]
    list_per_page = 30


@admin.register(Refunds)
class RefundsAdmin(admin.ModelAdmin):
    list_display = ("user_id", "external_refund_id", "amount", "currency", "status", "reason")
    list_display_links = ("user_id", "external_refund_id")
    ordering = ["created_at"]
    search_fields = ["user_id", "external_refund_id"]
    list_per_page = 30
