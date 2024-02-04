from contextlib import suppress
from typing import Any, Callable
from uuid import UUID

import structlog
from django.http import HttpRequest
from jose import JWTError, jwt

from config.auth import auth_settings


class AuthJWTMiddleware:
    get_response: Callable[[HttpRequest], Any]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        structlog.contextvars.clear_contextvars()
        jwt_user_id: str | None

        access_token = request.COOKIES.get("access_token", None)
        jwt_user_id = None

        if access_token:
            with suppress(JWTError):
                payload = jwt.decode(access_token, key=auth_settings.rsa_pub, algorithms=["RS256"])
                jwt_user_id = payload.get("sub")
        structlog.contextvars.bind_contextvars(jwt_user_id=jwt_user_id)

        request.jwt_user_id = UUID(jwt_user_id) if jwt_user_id else None
        response = self.get_response(request)

        return response
