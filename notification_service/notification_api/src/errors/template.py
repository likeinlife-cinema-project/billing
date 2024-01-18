from typing import Sequence

from fastapi import status

from .base import BaseError


class TemplateError(BaseError):
    ...


class TemplateNotFound(TemplateError):
    detail = {
        "message": "Template not found",
    }
    status_code = status.HTTP_404_NOT_FOUND


class NotEnoughParametersError(TemplateError):
    def __init__(
        self,
        required_params: Sequence[str],
        received_params: Sequence[str],
        *args,
    ) -> None:
        self.detail = {
            "message": "Not enough parameters",
            "required": required_params,
            "received": received_params,
        }

        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        super().__init__(*args)
