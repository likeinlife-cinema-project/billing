import uuid

from pydantic import BaseModel


class BaseNotificationDetails(BaseModel):
    id: uuid.UUID
    message: str
    to: str
    subject: str


class SMTPNotificationDetails(BaseNotificationDetails):
    from_: str
