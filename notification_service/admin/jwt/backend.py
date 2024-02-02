import http
import uuid

import requests
import structlog
from dependency_injector.wiring import Provide
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from config.auth import auth_settings

from .constants import ADMIN_ROLE
from .containers import AuthContainer
from .jwt_service import JWTService

User = get_user_model()


class JWTAuthBackend(BaseBackend):
    jwt_service: JWTService = Provide[AuthContainer.jwt_service]
    logger = structlog.get_logger()

    def authenticate(self, request: HttpRequest, username=None, password=None):
        payload = {"email": username, "password": password}
        headers = {"X-Request-Id": request.headers.get("X-Request-Id") or str(uuid.uuid4())}
        try:
            response = requests.post(auth_settings.login_url, json=payload, headers=headers, timeout=10)
            self.logger.debug(
                cookies=response.cookies,
                status=response.status_code,
                content=response.content,
            )
        except requests.RequestException:
            return None

        if response.status_code != http.HTTPStatus.OK:
            return None

        access_token = response.cookies.get("access_token")
        if not access_token:
            return None

        jwt_content = self.jwt_service.decode_access_token(access_token)

        try:
            user, created = User.objects.get_or_create(id=jwt_content["sub"])
            user.email = jwt_content["email"]
            user.is_admin = ADMIN_ROLE in jwt_content["roles"]
            user.is_active = True
            user.save()
        except Exception:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
