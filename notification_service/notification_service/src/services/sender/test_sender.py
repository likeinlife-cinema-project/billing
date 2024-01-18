import structlog
from container import Container
from dependency_injector.wiring import Provide, inject
from models import BaseNotificationDetails
from models.queue_message import UserProvidedQueueMessage

from ..notification_provider import TestProvider

logger = structlog.get_logger()


@inject
async def sender(
    message: UserProvidedQueueMessage,
    provider: TestProvider = Provide[Container.test_provider],
) -> bool:
    details = BaseNotificationDetails(
        id=message.id,
        message=message.message,
        subject=message.subject,
        to=message.user.email,
    )
    result = await provider.send(details)
    return result
