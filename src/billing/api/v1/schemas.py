import uuid

from pydantic import BaseModel, HttpUrl


class PaymentOutputSchema(BaseModel):
    url: HttpUrl
    payment_id: uuid.UUID
