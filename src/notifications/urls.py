from django.urls import path

from notifications.views import TestNotificationView

urlpatterns = [
    path("reminder/", TestNotificationView.as_view()),
]
