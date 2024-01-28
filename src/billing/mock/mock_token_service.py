import uuid

import structlog

from billing.config import settings_auth
from billing.services.abstracts import AbstractTokenService


class MockTokenService(AbstractTokenService):
    def __init__(self, public_key: str) -> None:
        self.logger = structlog.get_logger(__name__)
        self.public_key = public_key

    def get_user_id_from_token(self, access_token: str) -> str:
        user_id = str(uuid.uuid4())
        return user_id


def get_mock_token_service() -> MockTokenService:
    return MockTokenService(settings_auth.public_key)
