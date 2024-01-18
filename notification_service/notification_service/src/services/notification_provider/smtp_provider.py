from email.message import EmailMessage
from typing import Any

import aiosmtplib
from models import SMTPNotificationDetails

from .base_provider import BaseProvider


class SMTPProvider(BaseProvider):
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        login: str,
        password: str,
        logger: Any,
        use_tls: bool = False,
    ) -> None:
        self.logger = logger
        self.server = aiosmtplib.SMTP(
            hostname=smtp_host,
            port=smtp_port,
            username=login,
            password=password,
            use_tls=False,
        )

        if use_tls:
            self.server.use_tls = True

    async def send(self, details: SMTPNotificationDetails) -> bool:
        try:
            async with self.server:
                message = EmailMessage()
                message["From"] = details.from_
                message["To"] = ",".join([details.to])
                message["Subject"] = details.subject
                message.add_alternative(details.message)

                await self.server.send_message(message)
                self.logger.info("Message sent", id=details.id)
                return True
        except Exception as e:
            self.logger.error(e, exc_info=True)
            return False
