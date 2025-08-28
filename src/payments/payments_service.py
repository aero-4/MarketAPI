import logging
from uuid import uuid4

from fastapi import HTTPException
from starlette import status
from tortoise.transactions import in_transaction

from src.exceptions import NotFound
from src.models import User
from src.orders.models import OrderStatus, Order
from src.payments.enums import PaymentStatus
from src.payments.models import Payment
from src.payments.schemas import PaymentOut, CreatePaymentIn
from src.services.payment.bank import payment_provider


async def get_payment_info(payment_id: str) -> PaymentOut:
    p = await Payment.filter(id=payment_id).first()
    if not p:
        raise NotFound()

    return PaymentOut(
        payment_id=p.id,
        amount=p.amount,
        status=p.status,
    )


async def create_payment(schema: CreatePaymentIn, user: User, idempotency_key: str = None) -> PaymentOut:
    existing = await Payment.filter(idempotency_key=idempotency_key).first()
    if existing:
        return PaymentOut(
            payment_id=existing.id,
            amount=existing.amount,
            status=existing.status,
        )

    if not idempotency_key:
        idempotency_key = str(uuid4())

    payment_id = str(uuid4())

    async with in_transaction() as tx:
        payment = await Payment.create(
            id=payment_id,
            user=user,
            amount=schema.amount,
            idempotency_key=idempotency_key,
            using_db=tx
        )

        provider_resp = await payment_provider.create_payment(amount=schema.amount, idempotency_key=idempotency_key, metadata={})
        payment.provider_id = provider_resp.get("id")
        payment.status = provider_resp.get("status", PaymentStatus.PENDING)

        if provider_resp.get("status") == PaymentStatus.SUCCESS:
            user.balance += schema.amount
            payment.status = PaymentStatus.SUCCESS
            await user.save(using_db=tx)
            await payment.save(using_db=tx)


    return PaymentOut(
        payment_id=payment_id,
        amount=schema.amount,
        status=payment.status,
    )


async def process_webhook_event(event: dict) -> None:
    evt_type: str = event.get("type")
    data: dict = event.get("data", {})
    provider_payment_id: str = (data.get("id")
                                or data.get("object", {}).get("id"))
    metadata: dict = (data.get("metadata", {}) or
                      data.get("object", {}).get("metadata", {}))

    async with in_transaction() as tx:
        payment = None
        if provider_payment_id:
            payment = await Payment.filter(provider_id=provider_payment_id).using_db(tx).first()

        if not payment and metadata.get("payment_id"):
            payment = await Payment.filter(id=metadata["payment_id"]).using_db(tx).first()

        if not payment:
            raise Exception(f"Unknown payment by ID: {provider_payment_id}")

        if evt_type in ("payment.succeeded", "charge.succeeded"):
            payment.status = PaymentStatus.SUCCESS

        elif evt_type in ("payment.expired", "charge.expired"):
            payment.status = PaymentStatus.EXPIRED
        else:
            payment.status = PaymentStatus.FAIL

        await payment.save(using_db=tx)
