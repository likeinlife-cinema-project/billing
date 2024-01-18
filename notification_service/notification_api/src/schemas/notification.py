from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class NotifyStatusEnum(str, Enum):
    PG = "PG"
    OK = "OK"
    ER = "ER"


class NotifyStatusSchema(BaseModel):
    id: UUID
    subject: str
    status: NotifyStatusEnum
    description: str
