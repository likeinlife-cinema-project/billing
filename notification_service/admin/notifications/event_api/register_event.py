import uuid

import requests

from config.settings import NOTIFICATION_API_URL
from notifications.event_api.schemas import EventSchema
from notifications.models import Notification


def prepare_event_model(notification: Notification) -> EventSchema:
    return EventSchema(
        type_=notification.type.lower(),
        template=notification.template.slug,
        is_regular=True,
        subject=notification.subject,
        to_role=notification.roles,
        to_id=[],
        params={},
    )


def register_event(event: EventSchema) -> requests.Response:
    request_id = str(uuid.uuid4())
    response = requests.post(
        f"{NOTIFICATION_API_URL}/api/v1/events/",
        json=event.model_dump(),
        headers={"X-Request-Id": request_id},
        timeout=30,
    )
    return response
