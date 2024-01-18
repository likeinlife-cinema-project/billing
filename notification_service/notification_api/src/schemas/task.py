from enum import Enum
from typing import Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class NotifyType(str, Enum):
    EMAIL = "email"
    TEST = "test"


class TaskCreateSchema(BaseModel):
    type_: NotifyType
    template: str
    is_regular: bool
    subject: str
    to_role: list[str]
    to_id: list[UUID]
    params: Dict[str, str]


class TaskWithMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    is_regular: bool
    type_: NotifyType
    subject: str
    message: str
    to_id: list[UUID]
    to_role: list[str]


class TemplateSchema(BaseModel):
    slug: str
    content: str
    params: list[str]
