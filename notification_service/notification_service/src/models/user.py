import uuid

from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    id: uuid.UUID
    email: EmailStr
