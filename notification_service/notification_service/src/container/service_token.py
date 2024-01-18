from dataclasses import dataclass

import backoff
import httpx
import structlog
from core.settings import settings

logger = structlog.get_logger()


class CantGetAuthTokensError(Exception):
    ...


@dataclass
class Tokens:
    access_token: str
    refresh_token: str


@backoff.on_exception(
    backoff.expo,
    httpx.RequestError,
    max_time=10,
)
def get_service_token():
    with httpx.Client(base_url=settings.auth.get_base_url()) as client:
        sign_in_response = client.post(
            settings.auth.sign_in_route,
            json={
                "email": settings.auth.email,
                "password": settings.auth.password,
            },
        )

    access_token = sign_in_response.cookies.get("access_token")
    refresh_token = sign_in_response.cookies.get("refresh_token")

    if not access_token or not refresh_token:
        raise CantGetAuthTokensError

    logger.info("Got service auth tokens")
    return Tokens(access_token=access_token, refresh_token=refresh_token)
