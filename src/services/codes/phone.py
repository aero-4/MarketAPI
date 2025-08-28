import logging
import httpx

from src.config import settings


class Phone:

    def __init__(self, api_key: str = settings.NOTISEND_API_KEY, project_name: str = settings.NOTISEND_PROJECT):
        self.project_name = project_name
        self.api_key = api_key

    def message(self, code: int) -> str:
        return f"Ваш код подтверждения: {code} - никому его не сообщайте!"

    async def sent_code(self, phone: int, code: int) -> bool:
        files = {
            "project": (None, "BazarMarket"),
            "recipients": (None, str(phone)),
            "message": (None, self.message(code)),
            "apikey": (None, self.api_key),
        }

        headers = {"Accept": "application/json"}
        async with httpx.AsyncClient() as client:
            response = await client.post("https://sms.notisend.ru/api/message/send", headers=headers, files=files)
            data = response.json()
            if data.get("status") == 'error':
                raise ValueError(str(data.get("message")))

            logging.info(f"PhoneService: {phone} Sent code - {code} ({response.json()})")
            response.raise_for_status()
            return True
