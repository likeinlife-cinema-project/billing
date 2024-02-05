import json

from abc import ABC, abstractmethod

import requests
import structlog


class AbstractNotificator(ABC):
    _login_url: str
    _user_info_url: str
    _notification_api_url: str
    _email: str
    _password: str
    _logger: structlog.BoundLogger

    @abstractmethod
    def send_notification_request(
        self, type_: str, template: str, subject: str, user_id: str, params: dict, is_regular: bool = False
    ):
        pass


class Notificator(AbstractNotificator):
    def __init__(
        self, login_url: str, user_info_url: str, notification_api_url: str, email: str, password: str
    ) -> None:
        self._login_url = login_url
        self._user_info_url = user_info_url
        self._notification_api_url = notification_api_url
        self._email = email
        self._password = password
        self._logger = structlog.get_logger()

    def send_notification_request(
        self, type_: str, template: str, subject: str, user_id: str, params: dict, is_regular: bool = False
    ):
        access_token = self._get_access_token()
        if not access_token:
            self._logger.error("Ошибка получения access_token")
            return
        self._logger.info("Got access token", access_token=access_token)
        user_info = self._get_user_info(user_id=user_id, access_token=access_token)
        if not user_info:
            self._logger.error("Ошибка получения user_info")
            return
        self._logger.info("Got user_info", user_info=user_info)
        data = {
            "type_": type_,
            "template": template,
            "is_regular": is_regular,
            "subject": subject,
            "to_id": [user_id],
            "to_role": [],
            "params": {**user_info, **params},
        }
        self._logger.info("data", data=data)
        response = requests.post(url=self._notification_api_url, data=json.dumps(data), timeout=10)
        if response.status_code != 201:
            self._logger.error("Notification request fail for user", reason=response.json(), user_id=user_id)
            return
        self._logger.info("Notification request send to user", user_id=user_id)

    def _get_access_token(self) -> str:
        response = requests.post(
            url=self._login_url, data=json.dumps({"email": self._email, "password": self._password}), timeout=10
        )
        return response.cookies.get("access_token")

    def _get_user_info(self, user_id: str, access_token: str) -> dict:
        response = requests.get(
            url=f"{self._user_info_url}/{user_id}", cookies={"access_token": access_token}, timeout=10
        )
        user_info = response.json()
        return user_info
