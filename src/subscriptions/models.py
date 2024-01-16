from django.db import models
from models_mixins import TimeStampedMixin, UUIDMixin


class SubscriptionPeriods(models.Choices):
    month = "month"
    year = "year"


class Subscription(UUIDMixin, models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    description = models.TextField()
    amount = models.FloatField()
    period = models.TextField(choices=SubscriptionPeriods.choices, blank=False, null=False)


class UserSubscription(UUIDMixin, TimeStampedMixin, models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=False, null=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, blank=False, null=False)
    expire_at = models.DateTimeField()
    prolong = models.BooleanField()
