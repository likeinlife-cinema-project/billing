from copy import copy

import structlog

from django.http import HttpResponseRedirect
from dependency_injector.wiring import inject, Provide
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from billing.containers import Container
from billing.models import Payments, Refunds, Status
from billing.serializers import PaymentSerializer, RefundSerializer
from billing.services.abstracts import AbstractPaymentService, AbstractTokenService
from billing.schemas.payment import PaymentIn
from billing.schemas.refund import RefundIn


logger = structlog.get_logger(__name__)


class PaymentView(APIView):
    @extend_schema(request=PaymentIn)
    @inject
    def post(
        self,
        request: Request,
        format=None,  # noqa
        service: AbstractPaymentService = Provide[Container.payment_service],
        token_service: AbstractTokenService = Provide[Container.token_service],
    ):
        user_id = token_service.get_user_id_from_token(request.COOKIES.get("access_token"))  # noqa
        #  TODO если точно убираем user_id из запроса, и берем из токена, то добавить user_id к data
        payment_in = PaymentIn(**request.data)
        payment_out = service.request_payment(**payment_in.model_dump())
        serializer = PaymentSerializer(data=payment_out.model_dump(exclude=["confirmation", "payment_method_id"]))
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if payment_out.confirmation:
            serializer.save()
            return HttpResponseRedirect(payment_out.confirmation.confirmation_url)
        elif payment_out.payment_method_id:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error("Unknown behavior in payment processing")
            raise NotFound(detail="Unknown behavior in payment processing", code=status.HTTP_400_BAD_REQUEST)


class RefundView(APIView):
    @extend_schema(request=RefundIn)
    @inject
    def post(
        self,
        request: Request,
        format=None,  # noqa
        service: AbstractPaymentService = Provide[Container.payment_service],
    ):
        refund_in = RefundIn(**request.data)
        refund_out = service.refund_payment(**refund_in.model_dump())
        serializer = RefundSerializer(data=refund_out.model_dump())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationView(APIView):
    @inject
    def post(
        self,
        request: Request,
        format=None,  # noqa
        service: AbstractPaymentService = Provide[Container.payment_service],
    ):
        ip = request._request.headers.get("X-Forwarded-For")
        service.verify_incoming_ip(ip)
        data = copy(request.data)
        logger.info(f"{data=}")
        notification = service.process_notification(data)
        if notification.type == "payment":
            payment = Payments.objects.filter(external_payment_id=notification.id).first()
            payment.status = Status.need_confirm
            payment.refundable = notification.refundable
            payment.payment_method_id = notification.payment_method_id
            payment.payment_method = notification.payment_method_type
            payment.save()
        elif notification.type == "refund":
            refund = Refunds.objects.filter(external_refund_id=notification.id).first()
            refund.status = "need_confirm"
            refund.save()
        return Response({"detail": "notification received"}, status=status.HTTP_200_OK)
