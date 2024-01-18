from fastapi import status

from .base import BaseError


class NotificationError(BaseError):
    ...


class NotificationNotFound(NotificationError):
    detail = {
        "message": "Notification not found",
    }
    status_code = status.HTTP_404_NOT_FOUND
