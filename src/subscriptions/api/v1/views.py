from uuid import UUID

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets

from subscriptions.models import Subscription, UserSubscription
from subscriptions.serializers import SubscriptionSerializer, UserSubscriptionSerializer


class SubscriptionView(viewsets.ReadOnlyModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @extend_schema(parameters=[OpenApiParameter(name="id", type=UUID, location=OpenApiParameter.PATH)])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class UserSubscriptionView(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSubscriptionSerializer

    @extend_schema(parameters=[OpenApiParameter(name="id", type=UUID, location=OpenApiParameter.PATH)])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return UserSubscription.objects.filter(user_id=self.request.jwt_user_id)
