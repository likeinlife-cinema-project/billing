from django.urls import path, include
from rest_framework import routers

from subscriptions.views import SubscriptionView, UserSubscriptionView

subscriptions_router = routers.DefaultRouter()
subscriptions_router.register(r"subscriptions", SubscriptionView)

user_subscriptions_router = routers.DefaultRouter()
user_subscriptions_router.register(r"user_subscriptions", UserSubscriptionView, basename="user_subscriptions")

urlpatterns = [path("", include(subscriptions_router.urls)), path("", include(user_subscriptions_router.urls))]
