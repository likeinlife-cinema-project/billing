from typing import Any


class BaseError(Exception):
    detail: dict[str, Any]
    status_code: int
