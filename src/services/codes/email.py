import logging
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Iterable, Union, List

import aiosmtplib

from src.config import settings


class Email:
    def __init__(self, app_email: str = settings.EMAIL_APP, app_password: str = settings.PASSWORD_APP, smtp_server: str = settings.SMTP_SERVER, port: int = settings.SMTP_PORT):
        self.smtp_server = smtp_server
        self.port = port
        self.app_email = app_email
        self.app_password = app_password
        self.tls_context = ssl.create_default_context()

    def get_body(self, url: str) -> str:
        return f'Перейдите по ссылке чтобы подтвердить почту: <a href="{url}">НАЖМИТЕ ЗДЕСЬ</a>'

    async def send_mail(self, to: Union[str, Iterable[str]], subject: str, url: str, html: bool = True) -> None:
        recipients: List[str] = [to] if isinstance(to, str) else list(to)

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.app_email
        msg["To"] = ", ".join(recipients)
        subtype = "html" if html else "plain"
        mail = self.get_body(url)
        msg.attach(MIMEText(mail, subtype, "utf-8"))

        smtp = aiosmtplib.SMTP(
            hostname=self.smtp_server,
            port=self.port,
            timeout=60,
            use_tls=True,
        )

        try:
            await smtp.connect()
            try:
                await smtp.starttls(tls_context=self.tls_context)
            except aiosmtplib.SMTPException as e:
                txt = str(e).lower()
                if "already using tls" not in txt and "connection already using tls" not in txt:
                    raise

            await smtp.login(self.app_email, self.app_password)
            await smtp.send_message(msg, recipients=recipients)

            logging.info(f"EmailService: Sent mail - {msg}")

        except Exception as ex:
            logging.error(f"EmailService: Error - {ex}")

        finally:
            try:
                await smtp.quit()
            except Exception:
                try:
                    await smtp.close()
                except Exception:
                    pass
