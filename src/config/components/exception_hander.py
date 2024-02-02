from http import HTTPStatus

import pydantic_core
import structlog
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.http.response import Http404
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from config.base_error import BaseError

logger: structlog.stdlib.BoundLogger
logger = structlog.get_logger()


def custom_exception_handler(exc: Exception, context):
    if isinstance(exc, pydantic_core.ValidationError):
        logger.debug(exc.json(), exc_info=True)
        return JsonResponse(data=exc.errors(include_url=False), status=HTTPStatus.UNPROCESSABLE_ENTITY, safe=False)
    elif isinstance(exc, BaseError):
        return JsonResponse(data=exc.get_message(), status=exc.status_code)
    elif isinstance(exc, APIException):
        response = exception_handler(exc, context)
        if response is not None:
            response.data["status_code"] = response.status_code
        return response
    elif isinstance(exc, Http404):
        return JsonResponse({"detail": exc.args[0]}, safe=False, status=HTTPStatus.NOT_FOUND)
    elif isinstance(exc, IntegrityError):
        return JsonResponse({"detail": "Integrity error"}, safe=False, status=HTTPStatus.BAD_REQUEST)
    logger.error(exc, exc_info=True)
    return JsonResponse(data={"detail": "Server error"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
