from http import HTTPStatus

from config.base_error import BaseError


class JWTError(BaseError):
    """Base class for JWT errors."""

    status_code: int = HTTPStatus.UNAUTHORIZED
    detail: str = "JWT Error"

    def get_message(self) -> dict[str, str]:
        return {"detail": self.detail}


class InvalidScopeError(JWTError):
    detail = "Invalid jwt scope"

    def __init__(self, scope: str) -> None:
        self.scope = scope

    def get_message(self) -> dict[str, str]:
        return {"detail": self.detail, "scope": self.scope}


class NoAccessTokenError(JWTError):
    detail = "No access token in cookies"


class InvalidTokenError(JWTError):
    detail = "Invalid token"
