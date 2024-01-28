from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel


class Confirmation(BaseModel):
    type: str
    confirmation_url: str


class PaymentIn(BaseModel):
    user_id: UUID
    recurrent: bool
    user_purchase_item_id: UUID
    amount: float
    currency: Literal["RUB", "USD", "EUR"]
    payment_method_id: Optional[str] = None


class PaymentOut(PaymentIn):
    external_payment_id: str
    refundable: bool
    status: Literal["canceled", "succeeded", "pending"]
    confirmation: Optional[Confirmation] = None
