from rest_framework import viewsets

from .models import Subscription, UserSubscription
from .serializers import SubscriptionSerializer, UserSubscriptionSerializer


class SubscriptionView(viewsets.ReadOnlyModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class UserSubscriptionView(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSubscriptionSerializer

    def get_queryset(self):
        return UserSubscription.objects.filter(user_id=self.request.user_id)
