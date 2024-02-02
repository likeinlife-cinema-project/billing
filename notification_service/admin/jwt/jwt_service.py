from jose import JWTError, jwt

from config.auth import auth_settings

from .errors import InvalidScopeError, InvalidTokenError, NoAccessTokenError


class JWTService:
    def __init__(self, public_key: str) -> None:
        self.public_key = public_key

    def decode_access_token(self, token: str | None) -> dict:
        if not token:
            raise NoAccessTokenError
        try:
            payload: dict = jwt.decode(token=token, key=self.public_key, algorithms=["RS256"])
        except JWTError:
            raise InvalidTokenError
        if payload["scope"] == "access_token":
            return payload
        raise InvalidScopeError(payload["scope"])


def get_jwt_service() -> JWTService:
    return JWTService(public_key=auth_settings.public_key)
