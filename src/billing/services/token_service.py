import structlog

from jose import jwt, JWTError

from billing.config import settings_auth
from billing.exceptions import UserTokenException
from billing.services.abstracts import AbstractTokenService


class TokenService(AbstractTokenService):
    def __init__(self, public_key: str) -> None:
        self.public_key = public_key
        self.logger = structlog.get_logger(__name__)

    def get_user_id_from_token(self, access_token: str) -> str:
        if not access_token:
            raise UserTokenException()
        try:
            payload = jwt.decode(access_token, settings_auth.public_key, algorithms=["RS256"])
            user_id = payload.get("sub")
            if not user_id:
                raise UserTokenException()
            return user_id
        except JWTError:
            raise UserTokenException()


def get_token_service() -> TokenService:
    return TokenService(settings_auth.public_key)
