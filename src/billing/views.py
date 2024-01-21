from copy import copy

import structlog

from django.http import HttpResponseRedirect
from dependency_injector.wiring import inject, Provide
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from billing.serializers import PaymentSerializer, RefundSerializer
from billing.services.payment_service import PaymentService
from billing.containers import Container

logger = structlog.get_logger()


class PaymentView(APIView):
    @inject
    def post(self, request: Request, format=None, service: PaymentService = Provide[Container.payment_service]):  # noqa
        data = copy(request.data)
        if data.get("payment_method_id"):
            result = service.request_payment(data, repeated=True)
            logger.info(f"{result=}")
            serializer = PaymentSerializer(data=result)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        result = service.get_payment_link(data)
        if not result:
            logger.error("Unknown behavior in payment processing")
            raise NotFound(detail="Unknown behavior in payment processing", code=status.HTTP_400_BAD_REQUEST)
        link, modified_data = result
        serializer = PaymentSerializer(data=modified_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(link)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefundView(APIView):
    @inject
    def post(self, request: Request, format=None, service: PaymentService = Provide[Container.payment_service]):  # noqa
        data = copy(request.data)
        modified_data = service.refund_payment(data)
        if not modified_data:
            service.logger.error("Unknown behavior in refund processing")
            raise NotFound(detail="Unknown behavior in refund processing", code=status.HTTP_400_BAD_REQUEST)
        logger.info(f"refund data to queue: {modified_data}")
        serializer = RefundSerializer(data=modified_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationView(APIView):
    @inject
    def post(self, request: Request, format=None, service: PaymentService = Provide[Container.payment_service]):  # noqa
        logger.info(f"headeres = {request._request.headers}")
        service.verify_incoming_ip(request)
        logger.info(f"{request.data=}")
        service.process_notification(request.data)
        return Response({"detail": "notification received"}, status=status.HTTP_200_OK)
