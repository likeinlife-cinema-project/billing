import uuid

import structlog
from fastapi import Depends
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from structlog.stdlib import BoundLogger

from auth_app.db.sqlalchemy import get_async_session
from auth_app.errors.external import AlreadyExistingSocialNet, SocialnetNotFound
from auth_app.models.domain import Socialnet


class SocialnetRepository:
    def __init__(self, session: AsyncSession, logger: BoundLogger) -> None:
        self.session = session
        self.logger = logger

    async def get(self, socialnet_id: uuid.UUID) -> Socialnet:
        result = await self.session.execute(select(Socialnet).where(Socialnet.id == socialnet_id))
        try:
            return result.scalar_one()
        except NoResultFound:
            raise SocialnetNotFound(socialnet_id)

    async def get_by_oauth_id(self, oauth_id: str) -> Socialnet:
        result = await self.session.execute(select(Socialnet).where(Socialnet.oauth_id == oauth_id))
        try:
            return result.scalar_one()
        except NoResultFound:
            raise SocialnetNotFound(oauth_id)

    async def create(
        self,
        user_id: uuid.UUID,
        oauth_id: str,
        email: str | None,
    ) -> Socialnet:
        socialnet = Socialnet(user_id=user_id, oauth_id=oauth_id, email=email)

        try:
            self.session.add(socialnet)
            await self.session.commit()
            await self.session.refresh(socialnet)
            self.logger.info("Create", socialnet_id=socialnet.id)
        except IntegrityError:
            raise AlreadyExistingSocialNet("%s %s" % (oauth_id, email))
        return socialnet

    async def delete(self, socialnet_id: uuid.UUID) -> bool:
        result = await self.session.execute(
            delete(Socialnet).where(Socialnet.id == socialnet_id).returning(Socialnet.id),
        )
        try:
            deleted_id = result.scalar_one()
        except NoResultFound:
            raise SocialnetNotFound(socialnet_id)

        await self.session.commit()
        self.logger.info("Delete", socialnet_id=socialnet_id)
        return True if deleted_id else False

    async def delete_by_oauth_id(self, oauth_id: str) -> bool:
        result = await self.session.execute(
            delete(Socialnet).where(Socialnet.oauth_id == oauth_id).returning(Socialnet.id),
        )
        try:
            deleted_id = result.scalar_one()
        except NoResultFound:
            raise SocialnetNotFound(oauth_id)

        await self.session.commit()
        if deleted_id:
            self.logger.info("Delete", oauth_id=oauth_id)
            return True
        self.logger.info("Cant delete", oauth_id=oauth_id)
        return False


async def get_socialnet_repository(session: AsyncSession = Depends(get_async_session)) -> SocialnetRepository:
    logger = structlog.get_logger()
    return SocialnetRepository(session=session, logger=logger)
