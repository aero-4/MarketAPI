import logging
from uuid import uuid4
from tortoise.transactions import in_transaction
from datetime import datetime, UTC
from typing import Optional

from src.exceptions import NotFound
from src.orders.models import Order, OrderStatus
from src.payments.enums import PaymentStatus
from src.payments.models import Payment
from src.payments.payments_service import get_payment_info, create_payment, process_webhook_event
from src.payments.schemas import PaymentOut, CreatePaymentIn, PaymentInfo
from src.services.payment.bank import payment_provider
from src.session.depends import validate_access_token

from fastapi import FastAPI, APIRouter, Header, HTTPException, BackgroundTasks, status, Depends

app = FastAPI()
payment_router = APIRouter(prefix="/payments", tags=["Payments"])


@payment_router.post("/webhook")
async def provider_webhook(schema: PaymentInfo, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_webhook_event, schema.dict())
    return {"received": True}


@payment_router.post("", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
async def create_payment_handler(schema: CreatePaymentIn, idempotency_key: Optional[str] = Header(None, convert_underscores=False), user=Depends(validate_access_token)):
    payment = await create_payment(schema, user, idempotency_key)
    return payment


@payment_router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment_handler(payment_id: str, user=Depends(validate_access_token), idempotency_key: Optional[str] = Header(None, convert_underscores=False)):
    info = await get_payment_info(payment_id)
    return info
