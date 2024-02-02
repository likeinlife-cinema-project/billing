from http import HTTPStatus

import structlog
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView

from jwt.decorators import require_jwt
from payment_prolongation.tasks import start_prolongation

logger = structlog.get_logger(__name__)


class StartProlongation(APIView):
    @require_jwt
    def post(
        self,
        request: Request,
        format=None,  # noqa
    ):
        start_prolongation()
        return JsonResponse(data={"status": "OK"}, status=HTTPStatus.OK)
