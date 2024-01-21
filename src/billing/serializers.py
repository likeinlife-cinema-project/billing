from rest_framework import serializers

from billing.models import Payments, Refunds


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class RefundSerializer(serializers.ModelSerializer):
    payment_id = serializers.UUIDField()

    class Meta:
        model = Refunds
        fields = ["user_id", "payment_id", "external_refund_id", "amount", "currency", "status", "reason"]
