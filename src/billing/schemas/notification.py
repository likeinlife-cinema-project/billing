from typing import Literal, Optional

from pydantic import BaseModel


class Notification(BaseModel):
    id: str
    type: Literal["payment", "refund"]
    payment_method_type: Optional[str] = None
    payment_method_id: Optional[str] = None
    refundable: Optional[bool] = None
