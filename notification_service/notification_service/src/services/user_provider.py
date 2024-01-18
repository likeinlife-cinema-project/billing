import uuid
from http import HTTPStatus
from typing import Any

import backoff
import httpx
from asyncpg import Pool
from container.service_token import Tokens
from core import settings as st
from models.user import UserInfo


class UserProvider:
    def __init__(
        self,
        logger: Any,
        connection_pool: Pool,
        tokens: Tokens,
    ) -> None:
        self.logger = logger
        self.connection_pool = connection_pool
        self.tokens = tokens

    @backoff.on_exception(backoff.expo, httpx.RequestError, max_time=15)
    async def from_id(self, id_: uuid.UUID) -> UserInfo | None:
        async with httpx.AsyncClient(
            base_url=st.auth.get_base_url(),
            cookies={"access_token": self.tokens.access_token},
        ) as client:
            path = f"/user/{id_}/"
            response = await client.get(path)

        if response.status_code != HTTPStatus.OK:
            self.logger.debug("User not found", id=id_)
            return None

        user_info = UserInfo(**response.json())
        self.logger.debug("User fetched", result=user_info, id=id_)
        return user_info

    @backoff.on_exception(backoff.expo, httpx.RequestError, max_time=15)
    async def from_role(self, role: str) -> list[UserInfo]:
        self.logger.debug("Try fetch", role=role)
        async with httpx.AsyncClient(
            base_url=st.auth.get_base_url(),
            cookies={"access_token": self.tokens.access_token},
        ) as client:
            path = f"/role/{role}/user"
            response = await client.get(path)

        if response.status_code != HTTPStatus.OK:
            self.logger.debug("User not found", slug=role)
            return None

        user_info_list = [UserInfo(**i) for i in response.json()]
        self.logger.debug("Users fetched", result=user_info_list, slug=role)
        return user_info_list
