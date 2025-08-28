from pydantic import BaseModel, Field


class CreatePaymentIn(BaseModel):
    amount: int = Field(..., gt=10, le=1_000_000)


class PaymentOut(BaseModel):
    payment_id: str
    amount: int = Field(..., gt=10, le=1_000_000)
    status: str


class PaymentData(BaseModel):
    id: int
    status: str
    amount: int
    currency: str


class PaymentInfo(BaseModel):
    event: str
    payment: PaymentData
