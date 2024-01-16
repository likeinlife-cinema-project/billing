import uuid

import structlog
from fastapi import Depends
from pydantic import EmailStr
from structlog.stdlib import BoundLogger

from auth_app.external.user_repository import (
    UserRepository,
    get_user_repository,
)
from auth_app.models.domain.user import User

from .hash_service import HashService, get_hash_service


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        hash_service: HashService,
        logger: BoundLogger,
    ) -> None:
        self.user_repository = user_repository
        self.hash_service = hash_service
        self.logger = logger

    async def get(self, user_id: uuid.UUID) -> User:
        """Get user by id."""
        user = await self.user_repository.get(user_id)
        return user

    async def get_by_email(self, user_email: EmailStr) -> User:
        """Get user by email."""
        user = await self.user_repository.get_by_email(user_email)
        return user

    async def get_list(self, limit: int, offset: int) -> list[User]:
        """Get user list."""
        user = await self.user_repository.get_list(limit, offset)
        return user

    async def create(self, email: EmailStr, password: str) -> User:
        """Create new user."""
        hashed_password = self.hash_service.hash(password)

        result = await self.user_repository.create(email, hashed_password)

        self.logger.info("Create user", email=result.email, id=result.id)
        return result

    async def update(
        self,
        user_id: uuid.UUID,
        new_email: EmailStr | None = None,
        new_password: str | None = None,
    ) -> User:
        """Update user."""
        if new_password:
            hashed_password = self.hash_service.hash(new_password)
        else:
            hashed_password = None

        user = await self.user_repository.update(user_id, new_email, hashed_password)

        self.logger.info("Update user", id=user.id)
        return user

    async def delete(
        self,
        user_id: uuid.UUID,
    ) -> bool:
        """Delete user."""
        result = await self.user_repository.delete(user_id)

        self.logger.info("Delete user", id=user_id)
        return result


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    hash_service: HashService = Depends(get_hash_service),
) -> UserService:
    logger = structlog.get_logger()
    return UserService(
        user_repository=user_repository,
        hash_service=hash_service,
        logger=logger,
    )
