import structlog
from container import Container
from dependency_injector.wiring import Provide, inject
from models import SMTPNotificationDetails
from models.queue_message import UserProvidedQueueMessage

from ..notification_provider import SMTPProvider

logger = structlog.get_logger()


@inject
async def sender(
    message: UserProvidedQueueMessage,
    provider: SMTPProvider = Provide[Container.smtp_provider],
) -> bool:
    details = SMTPNotificationDetails(
        id=message.id,
        message=message.message,
        subject=message.subject,
        from_=message.user.email,
        to=message.user.email,
    )
    result = await provider.send(details)
    return result
