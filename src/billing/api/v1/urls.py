from django.urls import path

from .views import NotificationView, PaymentView, RefundView

urlpatterns = [
    path("payments/", PaymentView.as_view()),
    path("payments/refund/", RefundView.as_view()),
    path("payments/notification/", NotificationView.as_view()),
]
