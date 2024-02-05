import structlog

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.tasks import get_almost_expired_subsciptions, send_notification

logger = structlog.get_logger()


class TestNotificationView(APIView):
    def get(
        self,
        request: Request,
        format=None,  # noqa
    ):
        user_subscriptions = get_almost_expired_subsciptions()
        for user_subscription in user_subscriptions:
            send_notification(
                str(user_subscription.user_id),
                "email",
                "Payment-reminder",
                "Списание за продление подписки",
                {"subscription_name": user_subscription.subscription.name},
            )
        return Response(data={"detail": "OK"}, status=status.HTTP_200_OK)
