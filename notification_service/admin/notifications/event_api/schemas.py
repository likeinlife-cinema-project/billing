from uuid import UUID

from pydantic import BaseModel
import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseModelMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class EventSchema(BaseModel):
    type_: str
    template: str
    is_regular: bool
    subject: str
    to_role: list[str]
    to_id: list[UUID]
    params: dict[str, str]
