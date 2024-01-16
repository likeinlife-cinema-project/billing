import uuid

import structlog
from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from structlog.stdlib import BoundLogger

from auth_app.db.sqlalchemy import get_async_session
from auth_app.errors.external import UserNotHaveSocialNet
from auth_app.models.domain import Socialnet


class UserSocialnetRepository:
    def __init__(self, session: AsyncSession, logger: BoundLogger) -> None:
        self.session = session
        self.logger = logger

    async def get_user_socialnet(self, user_id: uuid.UUID) -> list[Socialnet]:
        result = await self.session.execute(
            select(Socialnet).where(Socialnet.user_id == user_id),
        )
        try:
            return result.scalars().all()
        except NoResultFound:
            raise UserNotHaveSocialNet(user_id)


async def get_user_socialnet_repository(session: AsyncSession = Depends(get_async_session)) -> UserSocialnetRepository:
    logger = structlog.get_logger()
    return UserSocialnetRepository(session=session, logger=logger)
