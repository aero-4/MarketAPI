import secrets
import time
import json
import hmac
import hashlib
from urllib.parse import urlencode

import httpx
from fastapi import FastAPI, Query

app = FastAPI()

WEBHOOK_SECRET: bytes = secrets.token_bytes(256)


def sign_hmac_sha256(secret: bytes, payload_bytes: bytes, with_ts: bool = True) -> tuple[str, str]:
    """
    Подпись в формате: sha256=<hex>
    Если with_ts=True, подпись делается по строке "{ts}.{raw_body}" (рекомендуется).
    Функция возвращает заголовок и timestamp.
    """
    ts = str(int(time.time()))
    if with_ts:
        signed = ts.encode("utf-8") + b"." + payload_bytes
    else:
        signed = payload_bytes
    sig_hex = hmac.new(secret, signed, hashlib.sha256).hexdigest()
    return f"sha256={sig_hex}", ts


@app.get("/send_json")
async def send_json(
        webhook_url: str = Query(..., description="URL куда банк шлёт webhook, e.g. https://example.com/webhook"),
        status: str = Query("succeeded", description="payment status: succeeded|failed|expired"),
        order_id: str = Query("ORDER-123"),
        amount: int = Query(1000),
        include_ts: bool = Query(True, description="подписывать с timestamp или нет")
):
    """
    Генерируем JSON webhook и отправляем с подписью.
    Пример:
    POST /send_json?webhook_url=URL
    """

    payload = {
        "event": f"payment.{status}",
        "payment": {
            "id": f"pay_{int(time.time())}",
            "order_id": order_id,
            "status": status,
            "amount": amount,
            "currency": "RUB",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    }

    content = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    signature_header, ts = sign_hmac_sha256(WEBHOOK_SECRET, content, with_ts=include_ts)

    headers = {
        "Content-Type": "application/json",
        "X-Hub-Signature-256": signature_header,
    }
    if include_ts:
        headers["X-Signature-Timestamp"] = ts

    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(webhook_url, data=payload, headers=headers, follow_redirects=True)

    return {"status_code": r.status_code,
            "resp_text": r.text,
            "sent_payload": payload,
            "headers_sent": headers}


@app.get("/send_form")
async def send_form(
    webhook_url: str = Query(...),
    status: str = Query("succeeded"),
    order_id: str = Query("ORDER-123"),
    amount: int = Query(1000),
    include_ts: bool = Query(False)
):
    """
    Генерируем form-urlencoded webhook и подписываем по form-байтам.
    Подпись делается по body (или по "ts.body" если include_ts=True).
    """
    data = {
        "event": f"payment.{status}",
        "payment_id": f"pay_{int(time.time())}",
        "order_id": order_id,
        "status": status,
        "amount": str(amount),
        "currency": "RUB"
    }

    content = urlencode(data).encode("utf-8")
    signature_header, ts = sign_hmac_sha256(WEBHOOK_SECRET, content, with_ts=include_ts)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Hub-Signature-256": signature_header,
    }
    if include_ts:
        headers["X-Signature-Timestamp"] = ts

    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(webhook_url, content=content, headers=headers, follow_redirects=True)
    return {"status_code": r.status_code, "resp_text": r.text, "sent_form": data, "headers_sent": headers}


