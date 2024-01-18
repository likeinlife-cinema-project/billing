import uuid

import structlog
from aio_pika.abc import AbstractIncomingMessage
from container import Container
from core import settings
from dependency_injector.wiring import Provide, inject
from models import QueueMessage
from models.notification_status import NotifyStatus, NotifyStatusEnum
from models.queue_message import UserProvidedQueueMessage
from pydantic import TypeAdapter
from services.producer import produce
from services.task_status_service import TaskStatusService
from services.user_provider import UserProvider

logger = structlog.get_logger()


async def resolver(
    message: AbstractIncomingMessage,
):
    """Resolve users."""
    logger.info("[x] Received message", id=message.message_id)
    adapted_message = TypeAdapter(QueueMessage).validate_json(message.body)
    logger.debug(adapted_message)

    await resolve_user_id(adapted_message)
    await resolve_role(adapted_message)
    await message.ack()


@inject
async def resolve_user_id(
    message: QueueMessage,
    user_provider: UserProvider = Provide[Container.user_provider],
    task_status: TaskStatusService = Provide[Container.task_status_service],
):
    """Resolve user ids."""
    for id_ in message.to_id:
        status = NotifyStatus(
            id=uuid.uuid4(),
            task_id=message.id,
            subject=message.subject,
            status=NotifyStatusEnum.PG,
            description="Provided user",
            type=str(message.type_).upper(),
        )
        user = await user_provider.from_id(id_)
        if not user:
            logger.warning("User not found", id=id_)
            status.status = NotifyStatusEnum.ER
            status.description = f"User {id_} not found"
            await task_status.upsert(status)
            continue

        formed_message = UserProvidedQueueMessage(
            task_id=message.id,
            id=uuid.uuid4(),
            user=user,
            type_=message.type_,
            message=message.message,
            subject=message.subject,
        )
        await produce(
            exchange_name=settings.queue.user_provided + "_exchange",
            message=formed_message.model_dump_json().encode(),
        )
        await task_status.upsert(status)


@inject
async def resolve_role(
    message: QueueMessage,
    user_provider: UserProvider = Provide[Container.user_provider],
    task_status: TaskStatusService = Provide[Container.task_status_service],
):
    """Resolve user roles."""
    for role in message.to_role:
        user_list = await user_provider.from_role(role)
        if not user_list:
            logger.warning("Users not found", role=role)
            status = NotifyStatus(
                id=uuid.uuid4(),
                task_id=message.id,
                subject=message.subject,
                status=NotifyStatusEnum.ER,
                description=f"Role {role} not found",
                type=str(message.type_.value).upper(),
            )
            await task_status.upsert(status)
            continue
        for user in user_list:
            message_id = uuid.uuid4()
            status = NotifyStatus(
                id=message_id,
                task_id=message.id,
                subject=message.subject,
                status=NotifyStatusEnum.PG,
                description="Provided user",
                type=str(message.type_.value).upper(),
            )
            formed_message = UserProvidedQueueMessage(
                task_id=message.id,
                id=message_id,
                user=user,
                type_=message.type_,
                message=message.message,
                subject=message.subject,
            )
            await produce(
                exchange_name=settings.queue.user_provided + "_exchange",
                message=formed_message.model_dump_json().encode(),
            )
            await task_status.upsert(status)
