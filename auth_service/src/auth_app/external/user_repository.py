import uuid

import structlog
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import selectinload
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from structlog.stdlib import BoundLogger

from auth_app.errors.external import AlreadyTakenEmail, UserNotFound

from ..db.sqlalchemy import get_async_session
from ..models.domain.user import User


class UserRepository:
    def __init__(self, session: AsyncSession, logger: BoundLogger) -> None:
        self.session = session
        self.logger = logger

    async def create(
        self,
        email: str,
        hashed_password: str,
    ) -> User:
        user = User(email=email, hashed_password=hashed_password)

        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            self.logger.info("Create user", user_id=user.id)
        except IntegrityError:
            raise AlreadyTakenEmail(email)
        return user

    async def get(self, user_id: uuid.UUID) -> User:
        result = await self.session.execute(select(User).where(User.id == user_id).options(selectinload(User.roles)))
        try:
            return result.scalar_one()
        except NoResultFound:
            raise UserNotFound(user_id)

    async def get_by_email(self, user_email: EmailStr) -> User:
        result = await self.session.execute(
            select(User)
            .where(User.email == user_email)
            .options(
                selectinload(User.roles),
            ),
        )
        try:
            return result.scalar_one()
        except NoResultFound:
            raise UserNotFound(user_email)

    async def get_list(self, limit: int, offset: int) -> list[User]:
        result = await self.session.execute(select(User).limit(limit).offset(offset))
        return result.scalars().all()

    async def delete(self, user_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            delete(User).where(User.id == user_id).returning(User.id),
        )
        try:
            deleted_id = result.scalar_one()
        except NoResultFound:
            raise UserNotFound(user_id)

        await self.session.commit()
        if deleted_id:
            self.logger.info("Delete user", id=user_id)
            return True
        self.logger.warning("Cant delete user", id=user_id)
        return False

    async def update(
        self,
        user_id: uuid.UUID,
        email: str | None = None,
        hashed_password: str | None = None,
    ) -> User:
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        try:
            user = result.scalar_one()
        except NoResultFound:
            raise UserNotFound(user_id)

        if email:
            user.email = email
        elif hashed_password:
            user.hashed_password = hashed_password

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        self.logger.info("Update user", id=user_id)

        return user


def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    logger = structlog.get_logger()
    return UserRepository(session=session, logger=logger)
