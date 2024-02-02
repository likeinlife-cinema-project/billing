from http import HTTPStatus

import pydantic_core
import structlog
from django.http import JsonResponse
from rest_framework.views import exception_handler

from config.base_error import BaseError

logger: structlog.stdlib.BoundLogger
logger = structlog.get_logger()


def custom_exception_handler(exc: Exception, context):
    if isinstance(exc, pydantic_core.ValidationError):
        logger.debug(exc.json(), exc_info=True)
        return JsonResponse(data=exc.errors(include_url=False), status=HTTPStatus.UNPROCESSABLE_ENTITY, safe=False)

    if isinstance(exc, BaseError):
        return JsonResponse(data=exc.get_message(), status=exc.status_code)

    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code

    return response
