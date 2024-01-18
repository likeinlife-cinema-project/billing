import abc
from typing import Generic, TypeVar

from models import BaseNotificationDetails

T = TypeVar("T", bound=BaseNotificationDetails)


class BaseProvider(abc.ABC, Generic[T]):
    @abc.abstractmethod
    async def send(self, notification_details: T) -> bool:
        """Send notification to user.

        Args.
        ----
            notification_details: details needed to send notification

        Returns.
        -------
            True - ok, False - error.
        """
