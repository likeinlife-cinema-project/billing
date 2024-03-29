import random
from datetime import timedelta
from functools import lru_cache

import structlog
from fastapi import Depends
from structlog.stdlib import BoundLogger

from auth_app.external.storage import (
    BaseStorageRepository,
    get_storage_repository,
)

from .jwt_service import JWTService, get_jwt_service


class TokenBlacklistService:
    def __init__(
        self,
        storage: BaseStorageRepository,
        jwt_service: JWTService,
        logger: BoundLogger,
    ) -> None:
        self.storage = storage
        self.jwt_service = jwt_service
        self.logger = logger

    async def put(self, token: str) -> None:
        jti = self.jwt_service.decode_token(token)["jti"]
        timedelta_ = self.jwt_service.get_timedelta(token)
        timedelta_with_jitter = timedelta_ + timedelta(seconds=random.uniform(1.05, 1.5))  # noqa: S311
        await self.storage.put(jti, 1, timedelta_with_jitter)
        self.logger.info("Put token in blacklist", jti=jti)

    async def get(self, token: str) -> bool:
        jti = self.jwt_service.decode_token(token)["jti"]
        if await self.storage.get(jti) is not None:
            self.logger.info("Found token with jti=%s", jti)
            return True
        self.logger.info("No token in blacklist", jti=jti)
        return False


@lru_cache
def get_token_blacklist_service(
    storage: BaseStorageRepository = Depends(get_storage_repository),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> TokenBlacklistService:
    logger = structlog.get_logger()
    return TokenBlacklistService(
        storage=storage,
        jwt_service=jwt_service,
        logger=logger,
    )
