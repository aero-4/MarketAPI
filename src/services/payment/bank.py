import random
from typing import Dict, Any
from uuid import uuid4

from src.payments.enums import PaymentStatus


class FakePaymentProvider:

    async def create_payment(self, amount: str, metadata: dict, idempotency_key: str) -> dict:
        redirect_url = f"https://example.com"
        return {
            "id": "prov_" + uuid4().hex,
            "status": PaymentStatus.SUCCESS,
            "amount": amount,
            "client_secret": "secret_" + uuid4().hex,
            "redirect_url": redirect_url,
        }

    def verify_and_parse_webhook(self, raw_body: bytes, signature: str) -> Dict[str, Any]:
        import json
        return json.loads(raw_body.decode())


payment_provider = FakePaymentProvider()
