from django.urls import path

from billing.views import PaymentView, RefundView, NotificationView

urlpatterns = [
    path("payments/", PaymentView.as_view()),
    path("payments/refund/", RefundView.as_view()),
    path("payments/notification/", NotificationView.as_view()),
]
