from django.contrib import admin

from .models import Subscription, UserSubscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "amount",
        "period",
    )
    search_fields = ["name"]
    list_per_page = 30


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "subscription",
        "expire_at",
        "prolong",
    )
    ordering = ["created_at"]
    search_fields = ["user_id"]
    list_per_page = 30
