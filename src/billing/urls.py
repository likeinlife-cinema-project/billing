from django.urls import path

from billing.views import NotificationView, PaymentView, RefundView

urlpatterns = [
    path("v1/payments/", PaymentView.as_view()),
    path("v1/payments/refund/", RefundView.as_view()),
    path("v1/payments/notification/", NotificationView.as_view()),
]
