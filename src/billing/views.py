from copy import copy
from datetime import datetime
import structlog
from dependency_injector.wiring import Provide, inject
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from billing.containers import Container
from billing.exceptions import (
    PaymentFailureException,
    NotFoundPaymentException,
    WrongUserSubscriptionException,
    ExpiredSubscriptionException,
)
from billing.models import Payments, Refunds, Status
from billing.schemas.payment import PaymentIn
from billing.schemas.refund import RefundIn
from billing.serializers import PaymentSerializer, RefundSerializer
from billing.services.abstracts import AbstractPaymentService
from jwt.decorators import require_jwt
from payment_prolongation.tasks import get_last_payment
from subscriptions.models import Subscription, UserSubscription

logger = structlog.get_logger(__name__)


class PaymentView(APIView):
    @extend_schema(request=PaymentIn, responses=None)
    @require_jwt
    @inject
    def post(
        self,
        request: Request,
        format=None,  # noqa
        service: AbstractPaymentService = Provide[Container.payment_service],
    ):
        payment_in = PaymentIn(**request.data)
        subscription = get_object_or_404(Subscription, id=payment_in.user_purchase_item_id)
        payment_out = service.request_payment(
            user_id=request.jwt_user_id,
            recurrent=payment_in.recurrent,
            user_purchase_item_id=payment_in.user_purchase_item_id,
            amount=subscription.amount,
            currency="RUB",
        )
        serializer = PaymentSerializer(data=payment_out.model_dump())
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if payment_out.confirmation:
            serializer.save()
            return HttpResponseRedirect(payment_out.confirmation.confirmation_url)
        else:
            logger.error("No confirmation", payment_out=payment_out, payment_in=payment_in)
            raise PaymentFailureException()


class RefundView(APIView):
    @extend_schema(request=RefundIn, responses=None)
    @require_jwt
    @inject
    def post(
        self,
        request: Request,
        format=None,  # noqa
    ):
        refund_in = RefundIn(**request.data)
        last_payment = get_last_payment(request.jwt_user_id, refund_in.user_subscription_id)
        if not last_payment:
            logger.warning("Found subscription, not found payment", user_subscription_id=refund_in.user_subscription_id)
            raise NotFoundPaymentException()
        user_subscription = UserSubscription.objects.get(refund_in.user_subscription_id)
        if not user_subscription:
            logger.info("Wrong user subscription", user_subscription_id=refund_in.user_subscription_id)
            raise WrongUserSubscriptionException()
        if user_subscription.expire_at >= datetime.now():
            logger.info("User subscription is already expired")
            raise ExpiredSubscriptionException()
        refund_data = refund_in.model_dump()
        refund_data["payment_id"] = last_payment.id
        refund_data["user_id"] = request.jwt_user_id
        refund_data["user_subscription_id"] = refund_in.user_subscription_id

        serializer = RefundSerializer(data=refund_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationView(APIView):
    @extend_schema(request=None, responses=None, exclude=True)
    @inject
    def post(
        self,
        request: Request,
        format=None,  # noqa
        service: AbstractPaymentService = Provide[Container.payment_service],
    ):
        ip = request.META["REMOTE_ADDR"]
        service.verify_incoming_ip(ip)
        data = copy(request.data)
        logger.info("Webhook received notification data", data=data)
        notification = service.process_notification(data)
        if notification.type == "payment":
            payment = get_object_or_404(Payments, external_payment_id=notification.id)
            payment.status = Status.need_confirm
            payment.refundable = notification.refundable
            payment.payment_method_id = notification.payment_method_id
            payment.payment_method = notification.payment_method_type
            payment.save()
        elif notification.type == "refund":
            refund = get_object_or_404(Refunds, external_refund_id=notification.id)
            refund.status = "need_confirm"
            refund.save()
        return Response({"detail": "notification received"}, status=status.HTTP_200_OK)
