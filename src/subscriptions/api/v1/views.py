from uuid import UUID

from dependency_injector.wiring import inject
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets

from jwt.decorators import require_jwt
from subscriptions.models import Subscription, UserSubscription
from subscriptions.serializers import SubscriptionSerializer, UserSubscriptionSerializer

from ..paginator import StandardResultsSetPagination


class SubscriptionView(viewsets.ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().order_by("id")
    serializer_class = SubscriptionSerializer
    pagination_class = StandardResultsSetPagination

    @extend_schema(parameters=[OpenApiParameter(name="id", type=UUID, location=OpenApiParameter.PATH)])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class UserSubscriptionView(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSubscriptionSerializer
    pagination_class = StandardResultsSetPagination

    @extend_schema(parameters=[OpenApiParameter(name="id", type=UUID, location=OpenApiParameter.PATH)])
    @require_jwt
    @inject
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @require_jwt
    @inject
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return UserSubscription.objects.filter(user_id=self.request.jwt_user_id).order_by("id")
