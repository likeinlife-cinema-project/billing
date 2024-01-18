import uuid
from enum import Enum

from pydantic import BaseModel


class NotifyStatusEnum(str, Enum):
    PG = "PG"
    OK = "OK"
    ER = "ER"


class NotifyTypeEnum(str, Enum):
    EMAIL = "EMAIL"
    WEBSOCKET = "WEBSOCKET"
    TEST = "TEST"


class NotifyStatus(BaseModel):
    id: uuid.UUID
    task_id: uuid.UUID
    subject: str
    status: NotifyStatusEnum
    description: str | None
    type: NotifyTypeEnum
