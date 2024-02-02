from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel


class Confirmation(BaseModel):
    type: str
    confirmation_url: str


class PaymentIn(BaseModel):
    recurrent: bool
    user_purchase_item_id: UUID


class PaymentOut(PaymentIn):
    user_id: UUID
    external_payment_id: str
    refundable: bool
    status: Literal["canceled", "succeeded", "pending"]
    confirmation: Optional[Confirmation] = None
    amount: float
    currency: Literal["RUB", "USD", "EUR"]
