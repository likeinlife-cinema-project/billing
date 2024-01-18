import logging
from http import HTTPStatus

from django.utils import timezone
from pydantic import ValidationError
from requests.exceptions import RequestException

from notifications.celery import app
from notifications.enums.notification_registration_status import NotificationRegistrationStatus
from notifications.event_api.register_event import prepare_event_model, register_event
from notifications.models import Notification

logger = logging.getLogger(__name__)


@app.task
def send_notifications():
    current_datetime = timezone.now()
    notifications = Notification.objects.filter(
        status=NotificationRegistrationStatus.WAITING,
        start_at__lte=current_datetime,
    )
    for notification in notifications:
        try:
            event = prepare_event_model(notification)
            response = register_event(event)
            if response.status_code == HTTPStatus.CREATED:
                notification.status = NotificationRegistrationStatus.DONE
                logger.info(
                    "Success event register notification_id=%s",
                    notification.id,
                )
            else:
                notification.status = NotificationRegistrationStatus.FAILED
                logger.error(
                    "Event register failed, notification_id=%s. Response:\n%s",
                    notification.id,
                    response.text,
                )
            notification.save()
        except ValidationError as err:
            logger.error("Cant prepare model, notification_id=%s\nError: %s", notification.id, err)
        except RequestException as err:
            logger.error("Cant send request, notification_id=%s\nError: %s", notification.id, err)
        except Exception as err:
            logger.error("Unexpected error, notification_id=%s. Error: %s", notification.id, err)
