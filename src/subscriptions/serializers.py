from rest_framework import serializers

from .models import Subscription, UserSubscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "name", "description", "amount", "period"]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = UserSubscription
        fields = ["id", "user_id", "subscription", "expire_at", "prolong", "archived"]
