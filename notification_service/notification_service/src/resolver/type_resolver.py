import structlog
from aio_pika.message import IncomingMessage
from container.container import Container
from core import settings
from dependency_injector.wiring import Provide, inject
from misc.type_alias import SenderType
from models.notification_status import NotifyStatus, NotifyStatusEnum
from models.queue_message import UserProvidedQueueMessage
from pydantic import TypeAdapter
from services.sender import smtp_sender, test_sender
from services.task_status_service import TaskStatusService

logger = structlog.get_logger()


notification_resolve_ways: dict[str, SenderType] = {
    "email": smtp_sender.sender,
    "test": test_sender.sender,
}


def check_x_death_count(message: IncomingMessage) -> bool:
    headers = message.headers
    if headers.get("x-death") and headers["x-death"][0].get("count", 0) > settings.queue.dead_letter_max_count:
        return False
    return True


@inject
async def resolver(
    message: IncomingMessage,
    task_status: TaskStatusService = Provide[Container.task_status_service],
) -> None:
    """Resolve notification type."""
    logger.info("[x] Received message", id=message.message_id)
    logger.debug("Message", message=message)

    adapted_message = TypeAdapter(UserProvidedQueueMessage).validate_json(message.body)
    if not check_x_death_count(message):
        await task_status.upsert(
            notify=NotifyStatus(
                task_id=adapted_message.task_id,
                id=adapted_message.id,
                description="Dead-letter max count reached",
                status=NotifyStatusEnum.ER,
                subject=adapted_message.subject,
                type=str(adapted_message.type_.value).upper(),
            ),
        )
        logger.error(
            "Dead-letter max count reached",
            task_id=adapted_message.task_id,
            id=adapted_message.id,
        )
        return

    logger.debug(adapted_message)
    sender = notification_resolve_ways.get(adapted_message.type_)
    if not sender:
        notify = NotifyStatus(
            task_id=adapted_message.task_id,
            id=adapted_message.id,
            description=f"Type {adapted_message.type_} not found",
            status=NotifyStatusEnum.ER,
            subject=adapted_message.subject,
            type=str(adapted_message.type_.value).upper(),
        )
        await task_status.upsert(
            notify=notify,
        )
        logger.error("Notification type not found", type=adapted_message.type_)
        return

    result = await sender(adapted_message)
    if not result:
        return await message.reject()
    notify = NotifyStatus(
        task_id=adapted_message.task_id,
        id=adapted_message.id,
        description="OK",
        status=NotifyStatusEnum.OK,
        subject=adapted_message.subject,
        type=str(adapted_message.type_.value).upper(),
    )
    await task_status.upsert(
        notify=notify,
    )
    return await message.ack()
