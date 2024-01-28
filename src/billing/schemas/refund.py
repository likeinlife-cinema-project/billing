from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class RefundIn(BaseModel):
    user_id: UUID
    payment_id: UUID
    external_payment_id: str
    amount: float
    currency: Literal["RUB", "USD", "EUR"]
    reason: str


class RefundOut(BaseModel):
    user_id: UUID
    payment_id: UUID
    amount: float
    currency: Literal["RUB", "USD", "EUR"]
    reason: str
    status: Literal["canceled", "succeeded", "pending"]
    external_refund_id: str
