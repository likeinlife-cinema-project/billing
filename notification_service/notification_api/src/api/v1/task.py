from uuid import UUID

from fastapi import APIRouter, Depends, Path, status
from schemas.notification import NotifyStatusSchema
from schemas.task import TaskCreateSchema, TaskWithMessage
from services.queue_service import QueueService, get_queue_service
from services.task_status_service import TaskStatusService, get_task_status_service
from services.template_service import TemplateService, get_template_service

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def add_notify_task(
    event: TaskCreateSchema,
    queue_service: QueueService = Depends(get_queue_service),
    template_service: TemplateService = Depends(get_template_service),
) -> TaskWithMessage:
    template = await template_service.get_template_by_slug(event.template)
    message = await queue_service.add_task(event, template)

    return message


@router.get(
    "/{task_id}/",
    status_code=status.HTTP_200_OK,
)
async def get(
    task_id: UUID = Path(description="Идентификатор задачи"),
    task_status_service: TaskStatusService = Depends(get_task_status_service),
) -> list[NotifyStatusSchema]:
    return await task_status_service.by_id(task_id)
