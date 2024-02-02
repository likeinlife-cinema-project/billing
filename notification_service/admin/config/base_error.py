from http import HTTPStatus


class BaseError(Exception):
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    detail: str = "Server error"

    def get_message(self) -> dict[str, str]:
        return {"detail": self.detail}
