from functools import lru_cache
from typing import Any

import structlog
from aio_pika import Message
from core.settings import settings
from db.rabbit import AbstractChannel, get_channel
from errors.template import NotEnoughParametersError
from fastapi import Depends
from jinja2 import Template
from schemas.task import TaskCreateSchema, TaskWithMessage, TemplateSchema


class QueueService:
    def __init__(
        self,
        channel: AbstractChannel,
        queue_name: str,
        logger: Any,
    ):
        self.channel = channel
        self.queue_name = queue_name
        self.logger = logger

    async def add_task(self, event: TaskCreateSchema, template: TemplateSchema) -> TaskWithMessage:
        task = self._generate_message(event, template)
        await self.channel.default_exchange.publish(
            Message(body=task.model_dump_json().encode()),
            routing_key=self.queue_name,
        )
        self.logger.info("Add task to queue", id=task.id)
        return task

    def _generate_message(self, task: TaskCreateSchema, template: TemplateSchema) -> TaskWithMessage:
        if not self._check_params(template.params, task.params):
            raise NotEnoughParametersError(template.params, list(task.params.keys()))

        jinja_template = Template(template.content)
        return TaskWithMessage(
            is_regular=task.is_regular,
            type_=task.type_,
            subject=task.subject,
            message=jinja_template.render(**task.params),
            to_id=task.to_id,
            to_role=task.to_role,
        )

    @staticmethod
    def _check_params(required_params: list, received_params: dict) -> bool:
        return all(el in received_params for el in required_params)


@lru_cache
def get_queue_service(
    channel: AbstractChannel = Depends(get_channel),
):
    return QueueService(
        channel=channel,
        queue_name=settings.rabbit.queue_name,
        logger=structlog.get_logger(),
    )
