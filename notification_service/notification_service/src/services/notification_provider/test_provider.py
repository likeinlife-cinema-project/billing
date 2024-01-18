from typing import Any

from models import BaseNotificationDetails

from .base_provider import BaseProvider


class TestProvider(BaseProvider):
    def __init__(
        self,
        logger: Any,
    ) -> None:
        self.logger = logger

    async def send(self, details: BaseNotificationDetails) -> bool:
        print(f"Sending email to {details.to}")
        print("ID: ", details.id)
        print("Subject: ", details.subject)
        print(
            "Message:\n------\n",
            details.message,
            "\n------",
        )
        print("Sent email...")
        self.logger.info("Message sent", id=details.id)
        return True
